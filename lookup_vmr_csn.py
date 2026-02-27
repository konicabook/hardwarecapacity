import os
import csv
import re
from pathlib import Path

def extract_text_files_to_csv(folder_path, output_csv):
    """
    Extract values from all text files in a folder into a single CSV file.
    
    Args:
        folder_path: Path to the folder containing text files
        output_csv: Path to the output CSV file
    """
    data = []
    
    # Get all text files in the folder
    text_files = Path(folder_path).glob("*.txt")
    
    for file_path in text_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Extract values (adjust regex pattern based on your needs)
                values = content.strip().split('\n')
                data.append({
                    'filename': file_path.name,
                    'content': content,
                    'line_count': len(values)
                })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Write to CSV
    if data:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data extracted to {output_csv}")
    else:
        print("No text files found.")

if __name__ == "__main__":
    folder = "."  # Current folder, change as needed
    output = "output.csv"
    extract_text_files_to_csv(folder, output)