import sys
import time
from collections import defaultdict
from math import ceil

def process_file():
    start_time = time.time() 

    city_data = defaultdict(lambda: [float("inf"), 0, float("-inf"), 0]) 
    data = sys.stdin.read().splitlines()

    for line in data:
        city, score = line.split(";")
        score = float(score)
        score_int = int(score * 10)  

        stats = city_data[city]
        stats[0] = min(stats[0], score)   
        stats[1] += score_int             
        stats[2] = max(stats[2], score)   
        stats[3] += 1
                         
    output_file_path = "/usr/src/app/output/result.txt" 
    with open(output_file_path, "w") as f:
        f.write("\n".join(
            f"{city}={data[0]:.1f}/{ceil((data[1] / data[3]) * 0.1 * 10) / 10:.1f}/{data[2]:.1f}"
            for city, data in sorted(city_data.items())
        ) + "\n")

    end_time = time.time() 
    elapsed_time = round((end_time - start_time) * 1000, 2)  

    print(f"Processing time: {elapsed_time}ms") 
if __name__ == "__main__":
    process_file()
