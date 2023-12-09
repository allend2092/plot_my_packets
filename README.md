# plot_my_packets
Gather information from my ASA firewall, geo locate the ip addresses in the log and plot on a map (in-preogress)


# ASA IP Data Lookup Tool

## Overview

This repository contains a set of Python scripts designed to automate the process of extracting IP addresses from Cisco ASA logs, performing geolocation lookups for each IP address, and managing API usage. The project is intended to provide insights into network traffic by mapping IP addresses to geographical locations.

## Components

The repository consists of the following main components:

### `poll_asa_and_process_text.py`

This script connects to a Cisco ASA device, retrieves logs, and processes them to extract IP addresses. It filters out IPv6 addresses and private IP addresses as per RFC 1918. The script then saves the processed IP addresses to a file for further analysis.

### `ipDataLookup.py`

This script takes an IP address as input and performs a geolocation lookup using an external API. It checks if the IP address has already been looked up to avoid redundant API calls. The script also maintains a count of API calls made and the number of times each IP address has been looked up, storing this data in respective JSON files.

## Additional Script

For full functionality, an additional bash script is recommended to orchestrate the execution of these Python scripts. This bash script should:

1. Run `poll_asa_and_process_text.py` to fetch and process IP addresses from the ASA logs.
2. Iterate over each IP address in the processed list and execute `ipDataLookup.py` for each one.
3. Optionally, include a delay between API calls to manage API rate limits.

This bash script is ideal for scheduling via a cron job for regular, automated execution.

## Setup and Configuration

1. Ensure Python 3 is installed on your system.
2. Install required Python libraries as specified in the scripts.
3. Configure `asa_creds.json` with the necessary credentials for accessing the Cisco ASA device.
4. Set up the API key for IP geolocation in `my_api_key.json`.
5. Adjust file paths in the scripts as per your directory structure.

## Usage

Run `poll_asa_and_process_text.py` to start the process of log extraction and IP address processing. Then, use `ipDataLookup.py` for geolocation lookups of each IP address.

For automated and regular execution, set up a bash script as described and schedule it using cron or a similar scheduler.

## Note

This project is designed for educational and network analysis purposes. Ensure compliance with all relevant network policies and data privacy regulations when using these scripts.
