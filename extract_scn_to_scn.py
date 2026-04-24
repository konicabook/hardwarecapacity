import os
import csv
from pathlib import Path

def merge_text_files_to_csv(folder_path, output_csv):
    """
    Merge all text files in a folder into a single CSV file.
    
    Args:
        folder_path: Path to the folder containing text files
        output_csv: Path to the output CSV file
    """
    all_data = []
    
    # Iterate through all text files in the folder
    for file_path in Path(folder_path).glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    all_data.append([file_path.name, line])
    
    # Write to CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Content'])
        writer.writerows(all_data)
    
    print(f"Merged {len(all_data)} lines into {output_csv}")

if __name__ == "__main__":
    folder = input("Enter folder path: ")
    output = input("Enter output CSV filename (default: merged.csv): ") or "merged.csv"
    merge_text_files_to_csv(folder, output)