import csv
import concurrent.futures
import requests
from tqdm import tqdm

def check_url_status(url):
    try:
        response = requests.get(url, timeout=10)
        return url, response.status_code
    except requests.RequestException:
        return url, "Error"

def main(input_file, output_file):
    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    results = []  # Store results here

    # Use multi-threading to check URL status
    with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(total=len(urls), desc="Checking URLs") as pbar:
        for result in executor.map(check_url_status, urls):
            results.append(result)
            pbar.update(1)  # Update the progress bar

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['URL', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for url, status in results:
            writer.writerow({'URL': url, 'Status': status})

if __name__ == "__main__":
    input_file_path = "input.txt"  # Replace with your input file path
    output_file_path = "output.csv"  # Replace with your output file path

    main(input_file_path, output_file_path)
