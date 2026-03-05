import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import sys

#open folder and selevt csv file and read data into dataframe
root = tk.Tk()
root.withdraw()

file_path_Ap15 = filedialog.askopenfilename(
    title="Select AP15 CSV file",
    filetypes=[("CSV files", "*.csv")]
)

# Check if user cancelled
if not file_path_Ap15:
    print("You cancelled AP15 file selection.")
    sys.exit()   # Exit the program if no file is selected

file_path_Ap24 = filedialog.askopenfilename(
    title="Select AP24 CSV file",
    filetypes=[("CSV files", "*.csv")]
)

# Check if user cancelled
if not file_path_Ap24:
    print("You cancelled AP24 file selection.")
    sys.exit()   # Exit the program if no file is selected  
if not file_path_Ap15:
    print("You cancelled AP15 file selection.")
    sys.exit()   # Exit the program if no file is selected


# Read the two CSV files, skipping the first 8 rows
df1 = pd.read_csv(file_path_Ap15, skiprows=8)
df2 = pd.read_csv(file_path_Ap24, skiprows=8)


#remove column index 8-15
columns_needed = [
    "Last Association Time",
    "User",
    "MAC Address",
    "Vendor",
    "IP Address",
    "AP Name",
    "802.11 State",
    "SSID",
]

df1 = df1[columns_needed]
df2 = df2[columns_needed]

#print("df1 columns:", len(df1.columns))
#print("df2 columns:", len(df2.columns))

# Perform a full outer join (union)
result = pd.concat([df1, df2], ignore_index=True)

#add header into result file "Last Association Time	User	MAC Address	Vendor	IP Address	AP Name	802.11 State	SSID	Profile	Protocol	AP Map Location	Endpoint Type	Last Seen	AP MAC Address	AP IP Address	Device IP Address"

#select row if column ssid is value WFMA21 , WFMB24
result = result[result['SSID'].isin(['WFMA21', 'WFMB24'])]


#remove column index 8-15
result = result.drop(result.columns[8:16], axis=1)


# Device type from IP
result["ip_last3"] = pd.to_numeric(
    result["IP Address"].astype(str).str[-3:], errors="coerce"
)

conditions = [
    result["ip_last3"].between(131, 139),
    result["ip_last3"].between(146, 150),
    result["ip_last3"].between(161, 169),
]

choices = ["PDA", "GOT", "PDA_AUDIT"]

result["Device_type"] = np.select(conditions, choices, default="Unknown")

#remove column index 1 and 8
result = result.drop(result.columns[[1,8]], axis=1)

#rename column "Last Association Time" to "Last_Association_Time"
result = result.rename(columns={"Last Association Time": "Last_Association_Time"})

#rename column "MAC Address" to "MAC_Address"
result = result.rename(columns={"MAC Address": "MAC_Address"})

#rename column "Vendor" to "Vendor_Name"
result = result.rename(columns={"Vendor": "Vendor_Name"})

#rename column "IP Address" to "IP_Address"
result = result.rename(columns={"IP Address": "IP_Address"})

#rename column "AP Name" to "AP_Name"
result = result.rename(columns={"AP Name": "AP_Name"})

#rename column "802.11 State" to "State_802.11"
result = result.rename(columns={"802.11 State": "Device_State"})

#rename column "SSID" to "SSID_Name"
result = result.rename(columns={"SSID": "SSID_Name"})

#replace value in column "Device_State" if value is "Disassociated" to "Disconnected" else value is "Associated" to "Connected" 
result["Device_State"] = result["Device_State"].replace({
    "Disassociated": "Disconnected",
    "Associated": "Connected"
})

#insert new column after column "Last_Association_Time" with name "Disconnected_Time" and value with calculation of current time - last association time if device state is "Disconnected" else value is empty from Column "Last_Association_Time and Today date time"
from datetime import datetime
# 1 Remove ICT from text
result["Last_Association_Time_clean"] = result["Last_Association_Time"].str.replace(" ICT", "", regex=False)

# 2 Convert to datetime
result["Last_Association_Time_dt"] = pd.to_datetime(
    result["Last_Association_Time_clean"],
    format="%a %b %d %H:%M:%S %Y",
    errors="coerce"
)

# 3 Calculate date difference
result["datediff"] = (pd.Timestamp.now() - result["Last_Association_Time_dt"]).dt.days

#remove column index 1 and 8
result = result.drop(result.columns[[0,8]], axis=1)

#print count group by ssid and device type
print("Count group by SSID and Device Type:")
print(result.groupby(["SSID_Name", "Device_type"], dropna=False).size())
#print count only SSID_name WFMA21 group by device type
print("Count group by Device Type for SSID WFMA21:")
print(result[result["SSID_Name"] == "WFMA21"].groupby("Device_type", dropna=False).size())

#copy column named "MAC_Address" to new column named "MAC_Address_Clean"
result["MAC_Address_Clean"] = result["MAC_Address"]
result["MAC_Address_Clean"] = result["MAC_Address_Clean"].str.replace(":", "").str.upper()


#read sotifile and merge with result file
soti_file_path = filedialog.askopenfilename(
    title="Select SOTI CSV file",
    filetypes=[("CSV files", "*.csv")]
)
soti_df = pd.read_csv(soti_file_path)

#rename column "MAC Address" to "MAC_Address"
soti_df = soti_df.rename(columns={"Wifi MAC Address": "MAC_Address"})

#clean "MAC_Address" column by remove ":" and convert to upper case
soti_df["MAC_Address"] = soti_df["MAC_Address"].str.replace(":", "").str.upper()


# Merge by MAC Address
result = pd.merge(
    result,
    soti_df[["MAC_Address", "Model", "Enrollment Time", "Agent Disconnect Time", "IP Address"]],
    left_on="MAC_Address_Clean",
    right_on="MAC_Address",
    how="left"
)

# Secondary lookup using IP Address
result = pd.merge(
    result,
    soti_df[["IP Address", "Model"]].rename(columns={"Model": "Model_IP"}),
    left_on="IP_Address",
    right_on="IP Address",
    how="left"
)

# Fill missing model
result["Model"] = result["Model"].fillna(result["Model_IP"])

# Clean columns
result = result.drop(columns=["Model_IP", "IP Address_y","IP Address_x","MAC_Address_y"])

#print count group by ssid and model include null value or unknown value
print("Count group by SSID and Model:")
print(result.groupby(["SSID_Name", "Model"], dropna=False).size())

# Save the result to a new CSV file
result.to_csv(r'D:\ITH\tempdownload\result.csv', index=False)
#save to xlsx file
result.to_excel(r'D:\ITH\tempdownload\result.xlsx', index=False)

print("Merge completed. Result saved to result.csv and result.xlsx")