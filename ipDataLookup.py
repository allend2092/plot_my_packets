import json
import ipdata
import sys
import re
import os
from datetime import datetime

def is_valid_ip(ip):
    """Check if the provided string is a valid IP address."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def update_meta_data(ip, meta_file_path):
    """Update the lookup count for the IP address in the meta data file."""
    try:
        with open(meta_file_path, 'r+') as file:
            meta_data = json.load(file)
            meta_data[ip] = meta_data.get(ip, 0) + 1
            file.seek(0)
            json.dump(meta_data, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        with open(meta_file_path, 'w') as file:
            json.dump({ip: 1}, file, indent=4)

def decrement_api_counter(counter_file_path):
    """Decrement the API call counter and return the new count."""
    try:
        with open(counter_file_path, 'r+') as file:
            data = json.load(file)
            if data['api_calls'] > 0:
                data['api_calls'] -= 1
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                return data['api_calls']
            else:
                return 0
    except FileNotFoundError:
        print("Error: ip_data_counter.json file not found.")
        sys.exit(1)

# Directory containing the data_export files and meta file
directory = "/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/api_results"

# Check if an IP address is provided as a command line argument
if len(sys.argv) != 2 or not is_valid_ip(sys.argv[1]):
    print("Usage: python script.py <IP_ADDRESS>")
    print("Please provide a valid IP address.")
    sys.exit(1)

ip_address = sys.argv[1]

# Update the meta data file with the IP address lookup count
meta_file_path = os.path.join(directory, "data_export_meta.json")
update_meta_data(ip_address, meta_file_path)

# Decrement the API call counter
counter_file_path = os.path.join(directory, "ip_data_counter.json")
remaining_calls = decrement_api_counter(counter_file_path)
if remaining_calls <= 0:
    print("API call limit reached.")
    sys.exit(1)

# Read the API key from the JSON file
with open(os.path.join(directory, 'my_api_key.json'), 'r') as file:
    data_import = json.load(file)
    ipdata.api_key = data_import['api_key']

# Perform the IP data lookup
data_export = ipdata.lookup(ip_address)

# Print the country name
print(data_export.country_name)

# Generate a filename with the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data_export_{current_time}.json"

# Write data_export to a JSON file
with open(os.path.join(directory, filename), 'w') as file:
    json.dump(data_export, file, indent=4)
