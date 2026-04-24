import pandas as pd

csv_path = r"D:\ITH\tempdownload\ca\202603\vmr_hardware_poc_pos_joined.csv"
excel_path = r"D:\ITH\tempdownload\ca\202603\store_profile.xlsx"
output_path = r"D:\ITH\tempdownload\ca\202603\joined_store_profile.csv"

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

#drop column "I" , "J" , "K" , "L"
columns_to_drop = ["I", "J", "K", "L"]
result_df = result_df.drop(columns=columns_to_drop)

# Save the joined result
result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Joined data written to: {output_path}")
