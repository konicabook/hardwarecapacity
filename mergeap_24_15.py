import os
import sys
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd

SKIP_ROWS = 8
SSIDS = ["WFMA21", "WFMB24"]
COLUMNS_NEEDED = [
    "Last Association Time",
    "MAC Address",
    "Vendor",
    "IP Address",
    "AP Name",
    "802.11 State",
    "SSID",
]
RENAMES = {
    "MAC Address": "MAC_Address",
    "Vendor": "Vendor_Name",
    "IP Address": "IP_Address",
    "AP Name": "AP_Name",
    "802.11 State": "Device_State",
    "SSID": "SSID_Name",
}
SOTI_COLUMNS = ["Model", "Enrollment Time", "Agent Disconnect Time"]


def ask_open(title):
    path = filedialog.askopenfilename(title=title, filetypes=[("CSV files", "*.csv")])
    if not path:
        print(f"You cancelled: {title}.")
        sys.exit()
    return path


def clean_mac(series):
    return series.str.replace(":", "", regex=False).str.upper()


def load_ap(path):
    df = pd.read_csv(path, skiprows=SKIP_ROWS)
    return df[COLUMNS_NEEDED]


def classify_device(ip):
    last_octet = pd.to_numeric(ip.astype(str).str.rsplit(".", n=1).str[-1], errors="coerce")
    conditions = [
        last_octet.between(131, 139),
        last_octet.between(146, 150),
        last_octet.between(161, 169),
    ]
    return np.select(conditions, ["PDA", "GOT", "PDA_AUDIT"], default="Unknown")


def build_ap_table(path_ap15, path_ap24):
    result = pd.concat([load_ap(path_ap15), load_ap(path_ap24)], ignore_index=True)
    result = result[result["SSID"].isin(SSIDS)].rename(columns=RENAMES)

    result["Device_type"] = classify_device(result["IP_Address"])
    result["Device_State"] = result["Device_State"].replace(
        {"Disassociated": "Disconnected", "Associated": "Connected"}
    )

    # e.g. "Mon Jan 05 10:11:12 2026 ICT"
    association_time = result.pop("Last Association Time")
    result["Last_Association_Time_dt"] = pd.to_datetime(
        association_time.str.replace(" ICT", "", regex=False),
        format="%a %b %d %H:%M:%S %Y",
        errors="coerce",
    )
    result["datediff"] = (pd.Timestamp.now() - result["Last_Association_Time_dt"]).dt.days
    result["MAC_Address_Clean"] = clean_mac(result["MAC_Address"])
    return result


def add_soti_model(result, soti_path):
    soti = pd.read_csv(soti_path)
    soti["MAC_Address_Clean"] = clean_mac(soti["Wifi MAC Address"])

    by_mac = soti[["MAC_Address_Clean", *SOTI_COLUMNS]].drop_duplicates("MAC_Address_Clean")
    by_ip = (
        soti[["IP Address", "Model"]]
        .rename(columns={"IP Address": "IP_Address", "Model": "Model_IP"})
        .drop_duplicates("IP_Address")
    )

    result = result.merge(by_mac, on="MAC_Address_Clean", how="left")
    result = result.merge(by_ip, on="IP_Address", how="left")
    result["Model"] = result["Model"].fillna(result["Model_IP"])
    return result.drop(columns="Model_IP")


def print_summary(result):
    print("Count group by SSID and Device Type:")
    print(result.groupby(["SSID_Name", "Device_type"], dropna=False).size())
    print("Count group by Device Type for SSID WFMA21:")
    print(result[result["SSID_Name"] == "WFMA21"].groupby("Device_type", dropna=False).size())
    print("Count group by SSID and Model:")
    print(result.groupby(["SSID_Name", "Model"], dropna=False).size())


def main():
    root = tk.Tk()
    root.withdraw()

    path_ap15 = ask_open("Select AP15 CSV file")
    path_ap24 = ask_open("Select AP24 CSV file")

    result = build_ap_table(path_ap15, path_ap24)

    result = add_soti_model(result, ask_open("Select SOTI CSV file"))
    print_summary(result)

    save_path = filedialog.asksaveasfilename(
        title="Save Result As",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
    )
    if not save_path:
        print("You cancelled saving the result.")
        sys.exit()

    base = os.path.splitext(save_path)[0]
    result.to_csv(base + ".csv", index=False)
    result.to_excel(base + ".xlsx", index=False)
    print(f"Merge completed. Result saved to {base}.csv and {base}.xlsx")


if __name__ == "__main__":
    main()
