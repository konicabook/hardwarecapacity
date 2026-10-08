@echo off
rem Build dist\HardwareCapacity.exe (run from this folder, with the venv active)
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name HardwareCapacity ^
  --add-data "1_extract_ist_to_ist.py;." ^
  --add-data "2_extract_scn_to_scn.py;." ^
  --add-data "3_extract_vmr_to_hw.py;." ^
  --add-data "4_lookup_hw_pos_ist.py;." ^
  --add-data "5_lookup_hw_sc_ist.py;." ^
  --add-data "6_lookup_store_pos.py;." ^
  --add-data "7_lookup_store_sc.py;." ^
  --add-data "8_count_sc_pos_scanner_model.py;." ^
  --add-data "POS_Model.csv;." ^
  --add-data "SC_Model.csv;." ^
  app.py
