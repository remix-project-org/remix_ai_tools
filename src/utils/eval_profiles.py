import csv
from datetime import datetime
from statistics import mean, median, stdev
import argparse

parser = argparse.ArgumentParser(description="Analyze a CSV file containing request profiling data.")
parser.add_argument("file_path", type=str, help="Path to the CSV file to analyze", default="services/profile.csv")

def analyze_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append({
                    'datetime': datetime.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%S.%f'),
                    'endpoint': row['endpoint'],
                    'method': row['method'],
                    'total_request_time': float(row['total_request_time']),
                    'llm_duration': float(row['llm_duration']),
                    'llm_average_duration': float(row['llm_average_duration'])
                })
            except Exception as e:
                print(f"Error reading row: {row}")
                print(e)
                continue

    # Basic statistics
    total_requests = len(data)
    avg_request_time = mean(row['total_request_time'] for row in data)
    median_request_time = median(row['total_request_time'] for row in data)
    std_dev_request_time = stdev(row['total_request_time'] for row in data)

    avg_llm_duration = mean(row['llm_duration'] for row in data)
    median_llm_duration = median(row['llm_duration'] for row in data)
    std_dev_llm_duration = stdev(row['llm_duration'] for row in data)

    # Time range
    start_time = min(row['datetime'] for row in data)
    end_time = max(row['datetime'] for row in data)
    time_range = end_time - start_time

    # Print results
    print(f"Total requests: {total_requests}")
    print(f"Time range: {time_range}")
    print(f"\nRequest Time Statistics:")
    print(f"  Average: {avg_request_time:.3f} seconds")
    print(f"  Median: {median_request_time:.3f} seconds")
    print(f"  Standard Deviation: {std_dev_request_time:.3f} seconds")
    print(f"\nLLM Duration Statistics:")
    print(f"  Average: {avg_llm_duration:.3f} seconds")
    print(f"  Median: {median_llm_duration:.3f} seconds")
    print(f"  Standard Deviation: {std_dev_llm_duration:.3f} seconds")

    # Additional analysis
    print("\nEndpoint Analysis:")
    endpoints = set(row['endpoint'] for row in data)
    for endpoint in endpoints:
        endpoint_data = [row for row in data if row['endpoint'] == endpoint]
        print(f"  {endpoint}:")
        print(f"    Total requests: {len(endpoint_data)}")
        print(f"    Average request time: {mean(row['total_request_time'] for row in endpoint_data):.3f} seconds")

if __name__ == "__main__":
    args = parser.parse_args()
    file_path = args.file_path
    analyze_csv(file_path)