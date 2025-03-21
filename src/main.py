import os
import mmap
import multiprocessing
from time import monotonic
from decimal import Decimal, getcontext, ROUND_DOWN

# Increase precision to reduce intermediate rounding errors
getcontext().prec = 50

def find_latest_testcase():
    """Find the latest generated testcase file in the testcases directory."""
    testcases_dir = "/usr/src/app/testcases"
    try:
        files = [f for f in os.listdir(testcases_dir) if f.startswith("testcase_")]
        if not files:
            raise FileNotFoundError("No testcase files found.")
        files.sort(key=lambda f: os.path.getctime(os.path.join(testcases_dir, f)), reverse=True)
        return os.path.join(testcases_dir, files[0])
    except Exception as e:
        print(f"Error finding testcase file: {e}")
        exit(1)

def process_chunk(start, end, file_path):
    """Process a chunk of the file."""
    city_map = {}
    with open(file_path, "rb") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # Align chunk boundaries to newline characters
        if start > 0:
            while start > 0 and mmapped_file[start - 1] != ord(b'\n'):
                start -= 1
        if end < len(mmapped_file):
            while end < len(mmapped_file) and mmapped_file[end] != ord(b'\n'):
                end += 1
        chunk = mmapped_file[start:end]
        lines = chunk.split(b'\n')
        for line in lines:
            if not line.strip():
                continue
            semicolon_idx = line.find(b';')
            if semicolon_idx == -1:
                continue  # Skip malformed lines
            city = line[:semicolon_idx]
            score_str = line[semicolon_idx + 1:]
            try:
                # Parse the score with high precision
                score = Decimal(score_str.decode().strip())
            except Exception:
                continue  # Skip invalid numbers
            if city not in city_map:
                city_map[city] = [score, score, score, 1]  # min, total, max, count
            else:
                stats = city_map[city]
                stats[0] = min(stats[0], score)
                stats[1] += score
                stats[2] = max(stats[2], score)
                stats[3] += 1
    return city_map

def merge_results(results):
    """Merge results from multiple processes."""
    final_map = {}
    for city_map in results:
        for city, stats in city_map.items():
            if city not in final_map:
                final_map[city] = stats[:]  # Copy the list
            else:
                final_stats = final_map[city]
                final_stats[0] = min(final_stats[0], stats[0])
                final_stats[1] += stats[1]
                final_stats[2] = max(final_stats[2], stats[2])
                final_stats[3] += stats[3]
    return final_map

def process_file():
    """Main function to process the input file."""
    start_time = monotonic()
    testcase_file = find_latest_testcase()
    with open(testcase_file, "rb") as f:
        file_size = os.fstat(f.fileno()).st_size
    num_workers = os.cpu_count() * 2
    chunk_size = file_size // num_workers
    offsets = [(i * chunk_size, (i + 1) * chunk_size if i < num_workers - 1 else file_size)
               for i in range(num_workers)]
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.starmap(process_chunk, [(start, end, testcase_file) for start, end in offsets])
    final_results = merge_results(results)
    output_lines = []
    for city in sorted(final_results.keys()):
        stats = final_results[city]
        # Compute mean with high precision division
        raw_mean = stats[1] / Decimal(stats[3])
        # Use ROUND_DOWN (i.e. truncate) to align with expected behavior (e.g., 0.3845 becomes 0.3)
        min_val = stats[0].quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        mean_val = raw_mean.quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        max_val = stats[2].quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        # Debug log to check raw aggregated values
        print(f"DEBUG: {city.decode()} raw min={stats[0]}, raw mean={raw_mean}, raw max={stats[2]}")
        output_lines.append(f"{city.decode()}={min_val}/{mean_val}/{max_val}")
    output_path = "/usr/src/app/src/output.txt"  # Write output to src directory
    with open(output_path, "w") as f:
        f.write('\n'.join(output_lines) + '\n')
    elapsed_time_ms = (monotonic() - start_time) * 1000
    print(f"Processing time: {elapsed_time_ms:.2f} ms")

if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    process_file()
