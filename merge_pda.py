from pathlib import Path
import csv
import pandas as pd

vmr_folder = r"D:\OneDrive - CPALLGROUP\IT_Hardware\Asset_Management\hw_capa\04326\version_vmr_bak"
output_csv = r"D:\OneDrive - CPALLGROUP\IT_Hardware\Asset_Management\hw_capa\vmr_pda_poc.csv"

vmr_files = sorted(Path(vmr_folder).glob("S*.vmr"))

if not vmr_files:
    print("No .vmr files found")
    exit()

all_rows = []

for file in vmr_files:
    with open(file, 'r', encoding='latin-1') as f:   # use latin-1 to avoid decode errors
        lines = f.readlines()

        #want to extarct line start with PDA only
        for line in lines:
            if line.startswith("PDA"):
                log_line = line.strip().replace("=", "|")
                all_rows.append(log_line.split("|"))
                break


header = ["comname", "date", "time", "storeno", "UUID", "HHID", "MTSVersion", "os_name", "osversion", "brand", "model", "Net Framework", "Total SD Card", "Free SD Card", "value_10", "value_11", "percent_Backup Battery", "Serial Battery", "batter_cycle", "battery_health", "mac_address", "ipaddress", "Total Device Memory", "In use Device Memory", "Free Device Memory", "value_21", "Wifi Config Version", "Total Program Memory", "Inuse Program Memory", "Free Program Memory", "ssid", "Status"]
all_rows.insert(0, header)


#write output split column by | and save to csv
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter="|")
    writer.writerows(all_rows)

mc_dataframe = []
other_dataframe = []

for row in all_rows[1:]:
    if len(row) > 10 and row[10].startswith(("MC31", "MC32")):
        mc_dataframe.append(row)
    else:
        other_dataframe.append(row)

#drop column 10 from mc_dataframe
df_mc_pda = pd.DataFrame(mc_dataframe)
df_mc_pda = df_mc_pda.drop(columns=[5,11,12,13,14,15,16,17,18,19,22,23,24,25,27,28,29])

#headermc = ["comname", "date", "time", "storeno", "hardwareserial", "value_1", "osname", "osversion", "brand", "model", "macaddress", "ipaddress", "wificonfigversion", "ssid", "apconnected", "value_2", "value_3"]

#add header into df_mc_pda
mc_header = ["comname", "date", "time", "storeno", "hardwareserial", "value_1", "osname", "osversion", "brand", "model", "macaddress", "ipaddress", "wificonfigversion", "ssid", "apconnected", "value_2", "value_3"]
df_mc_pda.columns = mc_header

mc_output_csv = r"D:\OneDrive - CPALLGROUP\IT_Hardware\Asset_Management\hw_capa\vmr_pda_mc.csv"

df_mc_pda.to_csv(
    mc_output_csv,
    sep="|",
    index=False,
    encoding="utf-8"
)

#drop column 10 from mc_dataframe
df_other_pda = pd.DataFrame(other_dataframe)
df_other_pda = df_other_pda.drop(columns=[5,11,12,13,14,15,16,17,18,19,22,23,24,25,27,28,29,30,31,32,33])

#add header into df_mc_pda
other_dataframe_header = ["comname", "date", "time", "storeno", "hardwareserial", "value_1", "osname", "osversion", "brand", "model", "macaddress", "ipaddress", "wificonfigversion", "ssid", "apconnected"]
df_other_pda.columns = other_dataframe_header

other_output_csv = r"D:\OneDrive - CPALLGROUP\IT_Hardware\Asset_Management\hw_capa\vmr_pda_other.csv"
df_other_pda.to_csv(
    other_output_csv,
    sep="|",
    index=False,
    encoding="utf-8"
)

#union df_mc_pda and df_other_pda
df_union = pd.concat([df_mc_pda, df_other_pda], ignore_index=True)


#union 2 dataframes with specify header
union_header = ["comname", "date", "time", "storeno", "hardwareserial", "value_1", "osname", "osversion", "brand", "model", "macaddress", "ipaddress", "wificonfigversion", "ssid", "apconnected"]

df_mc_pda = df_mc_pda.iloc[:, :15]
df_other_pda = df_other_pda.iloc[:, :15]

df_mc_pda.columns = union_header
df_other_pda.columns = union_header

df_union = pd.concat([df_mc_pda, df_other_pda], ignore_index=True)


#write df_union to csv
union_output_csv = r"D:\OneDrive - CPALLGROUP\IT_Hardware\Asset_Management\hw_capa\vmr_pda_union.csv"
with open(union_output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter="|")
    writer.writerows(df_union.values.tolist())

print(f"Processed {len(vmr_files)} files")
print(f"Output saved to {output_csv}")