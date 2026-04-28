import os
import csv
from pathlib import Path

def merge_text_files_to_csv(folder_path, output_csv):
    """
    Merge all scn files in a folder into a single CSV file.
    
    Args:
        folder_path: Path to the folder containing scn files
        read file and merge all value in all file into 1 csv file with column name comname|store_id|Manufacturer|Model|serialhardware|date|time|model_name
        output_csv: Path to the output CSV file
        add header column name with delimeter is pipe | comname|store_id|Manufacturer|Model|serialhardware|date|time|model_name
    """
    all_data = []
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".scn"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:   # use utf-8 to avoid decode errors
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line:  # skip empty lines
                        all_data.append(line.split("|"))  # split by pipe and add to all_data


    #add header column name with delimeter is pipe | comname|store_id|Manufacturer|Model|serialhardware|date|time|model_name
    header = ['comname', 'store_id', 'Manufacturer', 'Model', 'serialhardware', 'date', 'time','model_name']
    all_data.insert(0, header)
    
    #insert value into row of column model_name based on column model
    for row in all_data[1:]:  # skip header
        model = row[3] if len(row) > 3 else ""
        if "DS4308-SR00327PZWW" in model or "DS4308-SR00007PZAP" in model:
            row.append("Symbol DS4308")
        elif "1950g" in model:
            row.append("Honeywell 1950G")
        elif "1900" in model:
            row.append("Honeywell 1900")
        elif "1300" in model:
            row.append("Honeywell 1300")
        elif "MS7120 Barcode Scanner" in model or "MS7120 Barcode Scanner(keyboard mode)" in model:
            row.append("Symbol MS7120")
        else:
            row.append("Unknown Model")

    # Write output to CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerows(all_data)

    #with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    #    writer = csv.writer(csvfile)
    #    #writer.writerow(['Filename', 'Content'])
    #    writer.writerow(['Content'])
    #    writer.writerows(all_data)
    
    print(f"Merged {len(all_data)} lines into {output_csv}")

if __name__ == "__main__":
    folder = r"D:\ITH\tempdownload\ca\202604\sc_scn_5dgs_bak"
    output = r"D:\ITH\tempdownload\ca\202604\extract_scanner_data.csv"
    merge_text_files_to_csv(folder, output)