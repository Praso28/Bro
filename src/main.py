import sys
from collections import defaultdict
from math import ceil

def process_file():
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
                         
    sys.stdout.write("\n".join(
        f"{city}={data[0]:.1f}/{ceil((data[1] / data[3]) * 0.1 * 10) / 10:.1f}/{data[2]:.1f}"
        for city, data in sorted(city_data.items())
    ) + "\n")

if __name__ == "__main__":
    process_file()
