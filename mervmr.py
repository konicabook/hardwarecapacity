from pathlib import Path
import csv

vmr_folder = r"D:\ITH\vmr_file\202602\version_vmr"
output_csv = r"D:\ITH\vmr_file\202602\vmr_hardware_poc.csv"

vmr_files = sorted(Path(vmr_folder).glob("*.vmr"))

if not vmr_files:
    print("No .vmr files found")
    exit()

all_rows = []

for file in vmr_files:
    with open(file, 'r', encoding='latin-1') as f:   # use latin-1 to avoid decode errors
        lines = f.readlines()

        for i in range(len(lines)):
            if lines[i].strip() == "[Hardware]":
                if i + 1 < len(lines):
                    log_line = lines[i + 1].strip().replace("Log=", "")
                    all_rows.append(log_line.split("|"))
                break

#insert column header


header = ["comname", "Date", "Time", "Version", "model_name_raw", "CPU_Info", "CPU_Name", "CPU_Speed", "Memory", "BIOS_Info", "OS_Version", "Service_Pack", "OS_Name", "printer_type", "c_drive", "d_drive", "e_drive", "f_drive", "g_drive",  "h_drive",  "I", "J", "K", "L","laser_printer_name"]
all_rows.insert(0, header)

#insert comtype column based on comname column value   
header.insert(1, "comtype")

for row in all_rows[1:]:  # skip header
    comname = row[0]  # comname column
    if comname.startswith("P"):
        row.insert(1, "POS")  # insert comtype "POS" after comname column
    elif comname.startswith("S"):
        row.insert(1, "SC")  # insert comtype "SC" after comname column
    else:
        row.insert(1, "SC")  # insert comtype "Hardware Only" after comname column

# Write output
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(all_rows)

print(f"Processed {len(vmr_files)} files")
print(f"Output saved to {output_csv}")