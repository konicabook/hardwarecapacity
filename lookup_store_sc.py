import pandas as pd

csv_path = r"D:\ITH\tempdownload\ca\202604\vmr_sc_hardware_ist.csv"
excel_path = r"D:\ITH\tempdownload\ca\202604\store_profile.xlsx"
output_path = r"D:\ITH\tempdownload\ca\202604\vmr_sc_ist_store.csv"

# Read the source CSV and the store profile Excel file
pos_df = pd.read_csv(csv_path, dtype={"STORE_ID": str})
store_df = pd.read_excel(excel_path, dtype={"รหัสร้าน": str})

# Perform a left join on the specified keys
joined_df = pos_df.merge(
    store_df[["รหัสร้าน", "ชื่อสาขา", "ภาค", "สถานะร้านปัจจุบัน"]],
    how="left",
    left_on="STORE_ID",
    right_on="รหัสร้าน"
)

# Keep the original POS data plus the requested store profile columns
result_df = joined_df.assign(
    ชื่อสาขา=joined_df["ชื่อสาขา"],
    ภาค=joined_df["ภาค"],
    สถานะร้านปัจจุบัน=joined_df["สถานะร้านปัจจุบัน"]
)

# Optionally drop the duplicate join key column from the right table
result_df = result_df.drop(columns=["รหัสร้าน"])

#move column STORE_ID,ชื่อสาขา,ภาค,สถานะร้านปัจจุบัน to the front
cols = result_df.columns.tolist()
cols = ["STORE_ID", "ชื่อสาขา", "ภาค", "สถานะร้านปัจจุบัน"] + [col for col in cols if col not in ["STORE_ID", "ชื่อสาขา", "ภาค", "สถานะร้านปัจจุบัน"]]
result_df = result_df[cols]

# drop columns "I", "J", "K", "L" if they exist
columns_to_drop = ["I", "J", "K", "L"]
result_df = result_df.drop(columns=columns_to_drop, errors="ignore")

#insert column modelname after column model_name_raw and fill value from file C:\Users\rathasatekun\Documents\GitHub\hardwarecapacity\SC_Model.csv
model_df = pd.read_csv(r"C:\Users\rathasatekun\Documents\GitHub\hardwarecapacity\SC_Model.csv")
#lookup result_df wit model_df value is collum model lookup with result_df key is cpu_name and model_df key is cpu_code
result_df = result_df.merge(model_df[["cpu_code", "model"]], how="left", left_on="CPU_Info", right_on="cpu_code")
#drop column cpu_code
result_df = result_df.drop(columns=["cpu_code"])
#model column model after column model_name_raw
cols = result_df.columns.tolist()
model_name_raw_index = cols.index("model_name_raw")
cols.insert(model_name_raw_index + 1, cols.pop(cols.index("model")))
result_df = result_df[cols]

# Save the joined result
result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Joined data written to: {output_path}")
