import os
import json
import csv

source_folder = r'D:\ITH\tempdownload\ca\202603\sc_ist_5dgs_bak'  # Specify the source folder containing .ist files
output_file = r'D:\ITH\tempdownload\ca\202603\output_ist.csv'

# Define the headers based on the example
headers = [
    'STORE_ID', 'POS_NO', 'TERMINAL_NAME', 'TYPE', 'MACHINE_TAX_ID_SE',
    'MACHINE_TAX_ID_CS', 'STORE_TAX_ID_SE', 'STORE_TAX_ID_CS',
    'EFFECTIVE_DATETIME', 'CREATE_DATETIME', 'SERIAL_NO', 'CHK_DATE',
    'CHK_TIME', 'MAINBOARD_SERIAL_NO', 'ASSET_NO'
]

# Function to process a value: ltrim, rtrim, remove newlines and double quotes
def process_value(value):
    if isinstance(value, str):
        return value.strip().replace('\n', '').replace('"', '')
    return value

# Get all .ist files
ist_files = [f for f in os.listdir(source_folder) if f.endswith('.ist')]

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    for ist_file in ist_files:
        file_path = os.path.join(source_folder, ist_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Assuming each file contains a list of dicts
                for item in data:
                    processed_item = {key: process_value(item.get(key, '')) for key in headers}
                    writer.writerow(processed_item)
        except json.JSONDecodeError as e:
            print(f"Warning: Skipping {ist_file} - Invalid JSON: {e}")
        except Exception as e:
            print(f"Warning: Error processing {ist_file}: {e}")