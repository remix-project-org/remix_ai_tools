import csv, os, argparse
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

parser = argparse.ArgumentParser(description="Analyze a CSV file containing request profiling data.")
parser.add_argument("file_path", type=str, help="Path to the CSV file to analyze", default="services/profile.csv")

IMGS_DIR = "../imgs"
os.makedirs(IMGS_DIR, exist_ok=True)

def read_csv(file_path):
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
    return data

def plot_requests_over_time(data):
    daily_requests = defaultdict(int)
    for row in data:
        date = row['datetime'].date()
        daily_requests[date] += 1

    dates = sorted(daily_requests.keys())
    counts = [daily_requests[date] for date in dates]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker='o')
    plt.title('Total Requests per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGS_DIR,'requests_per_day.png'))
    plt.close()

def plot_average_request_time(data):
    daily_avg_times = defaultdict(list)
    for row in data:
        date = row['datetime'].date()
        daily_avg_times[date].append(row['total_request_time'])

    dates = sorted(daily_avg_times.keys())
    avg_times = [sum(daily_avg_times[date]) / len(daily_avg_times[date]) for date in dates]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_times, marker='o')
    plt.title('Average Request Time per Day')
    plt.xlabel('Date')
    plt.ylabel('Average Request Time (seconds)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGS_DIR,'avg_request_time_per_day.png'))
    plt.close()

def plot_requests_by_endpoint(data):
    endpoint_counts = defaultdict(int)
    for row in data:
        endpoint_counts[row['endpoint']] += 1

    endpoints = list(endpoint_counts.keys())
    counts = [endpoint_counts[endpoint] for endpoint in endpoints]

    plt.figure(figsize=(12, 6))
    plt.bar(endpoints, counts)
    plt.title('Total Requests by Endpoint')
    plt.xlabel('Endpoint')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGS_DIR, 'requests_by_endpoint.png'))
    plt.close()

def generate_metric_images(file_path):
    data = read_csv(file_path)
    plot_requests_over_time(data)
    plot_average_request_time(data)
    plot_requests_by_endpoint(data)
    print("Metric images have been generated and saved.")

if __name__ == "__main__":
    args = parser.parse_args()
    generate_metric_images(args.file_path)