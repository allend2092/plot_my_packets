#!/bin/bash

# Define the directory where your Python scripts are located
SCRIPT_DIR="/home/daryl/PycharmProjects/gpu_processing_tests/sub_projects"

# Navigate to the script directory
cd $SCRIPT_DIR

# Run the connect_to_asa_and_process.py script
python3 connect_to_asa_and_process.py

# Check if processed_ip_addresses.txt exists and is not empty
if [ -s "$SCRIPT_DIR/processed_ip_addresses.txt" ]; then
    # Read each line in processed_ip_addresses.txt and run ipDataLookup.py for each IP
    while IFS= read -r ip_address; do
        python3 ipDataLookup.py "$ip_address"
        sleep 1 # Pause for 1 second
    done < "$SCRIPT_DIR/processed_ip_addresses.txt"
else
    echo "No IP addresses to process."
fi
