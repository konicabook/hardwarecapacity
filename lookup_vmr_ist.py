import csv
from pathlib import Path


def main():
    left_path = Path(r"D:\ITH\tempdownload\ca\202603\vmr_hardware_poc_pos.csv")
    right_path = Path(r"D:\ITH\tempdownload\ca\202603\output_ist.csv")
    output_path = Path(r"D:\ITH\tempdownload\ca\202603\vmr_hardware_poc_pos_joined.csv")

    with left_path.open(newline='', encoding='utf-8') as left_file:
        left_reader = csv.DictReader(left_file)
        left_rows = list(left_reader)
        left_fieldnames = left_reader.fieldnames or []

    with right_path.open(newline='', encoding='utf-8') as right_file:
        right_reader = csv.DictReader(right_file)
        right_rows = list(right_reader)

    right_map = {
        row.get("TERMINAL_NAME", ""): {
            "MAINBOARD_SERIAL_NO": row.get("MAINBOARD_SERIAL_NO", ""),
            "ASSET_NO": row.get("ASSET_NO", ""),
        }
        for row in right_rows
        if row.get("TERMINAL_NAME", "")
    }

    extra_columns = ["MAINBOARD_SERIAL_NO", "ASSET_NO"]
    output_fieldnames = list(left_fieldnames)
    for col in extra_columns:
        if col not in output_fieldnames:
            output_fieldnames.append(col)

    #drop columns I,J,K,L
    output_fieldnames = [col for col in output_fieldnames if col not in ["I", "J", "K", "L"]]

    with output_path.open('w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=output_fieldnames)
        writer.writeheader()

        for left_row in left_rows:
            key = left_row.get("comname", "")
            right_values = right_map.get(key, {})
            merged_row = {**left_row}
            merged_row.update(right_values)
            writer.writerow(merged_row)


    print(f"Left join complete. Output written to: {output_path}")


if __name__ == "__main__":
    main()
