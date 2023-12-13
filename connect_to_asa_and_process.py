import json
import re
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def extract_ips(text):
    """
    Extract IPv4 addresses from the given text using a regular expression.
    """
    ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    return re.findall(ip_regex, text)

def is_private_ip(ip):
    """
    Check if an IP is a private IP (RFC 1918).
    """
    private_ip_ranges = [
        re.compile(r'^10\.'),
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
        re.compile(r'^192\.168\.')
    ]
    return any(regex.match(ip) for regex in private_ip_ranges)

def remove_ips(ips, remove_list):
    """
    Remove specified IPs from the list.
    """
    return [ip for ip in ips if ip not in remove_list]

def main():
    # Load device credentials from asa_creds.json
    try:
        with open('/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/asa_creds.json', 'r') as file:
            asa_device = json.load(file)
    except FileNotFoundError:
        print("Error: asa_creds.json file not found.")
        return
    except json.JSONDecodeError:
        print("Error: JSON decoding error in asa_creds.json.")
        return

    # Attempt to connect to the device
    try:
        with ConnectHandler(**asa_device) as net_connect:
            # Enter enable mode
            net_connect.enable()

            # Disable paging
            net_connect.send_command('terminal pager 0')

            # Execute the command
            output = net_connect.send_command('show logging asdm')
    except NetMikoTimeoutException:
        print("Connection timed out.")
        return
    except NetMikoAuthenticationException:
        print("Authentication failed.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Process the output
    ips = extract_ips(output)
    unique_ips = list(set(ips))
    public_ips = [ip for ip in unique_ips if not is_private_ip(ip)]

    # User-specified IPs to remove
    ips_to_remove = ['0.0.0.0', '75.70.165.33']  # Add IPs here that you want to remove

    # Remove user-specified IPs
    final_ips = remove_ips(public_ips, ips_to_remove)

    # Write the processed IPs to a file
    try:
        with open('/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects/processed_ip_addresses.txt', 'w') as file:
            for ip in final_ips:
                file.write(ip + '\n')
    except IOError:
        print("Error writing to processed_ip_addresses.txt.")
        return

if __name__ == "__main__":
    main()
