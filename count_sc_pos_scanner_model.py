import pandas as pd

# Count POS model
pos_file = r"D:\ITH\tempdownload\ca\202606\vmr_pos_ist_store.csv"
pos_df = pd.read_csv(pos_file)
pos_count = pos_df['model'].value_counts()
print("POS Model Count:")
print(pos_count)
print(f"\nTotal POS Records: {len(pos_df)}")

# Count SC model
sc_file = r"D:\ITH\tempdownload\ca\202606\vmr_sc_ist_store.csv"
sc_df = pd.read_csv(sc_file)
sc_count = sc_df['model'].value_counts()
print("\n\nSC Model Count:")
print(sc_count)
print(f"\nTotal SC Records: {len(sc_df)}")

# Count Scanner model in file D:\ITH\tempdownload\ca\202605\extract_scanner_data.csv count from column model_name and count value in column model_name and print count of each model_name and total record in file D:\ITH\tempdownload\ca\202605\extract_scanner_data.csv
scanner_file = r"D:\ITH\tempdownload\ca\202606\extract_scanner_data.csv"
scanner_df = pd.read_csv(scanner_file, delimiter='|')
scanner_count = scanner_df['model_name'].value_counts()
print("\n\nScanner Model Count:")
print(scanner_count)
print(f"\nTotal Scanner Records: {len(scanner_df)}")
