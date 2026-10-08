# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('1_extract_ist_to_ist.py', '.'), ('2_extract_scn_to_scn.py', '.'), ('3_extract_vmr_to_hw.py', '.'), ('4_lookup_hw_pos_ist.py', '.'), ('5_lookup_hw_sc_ist.py', '.'), ('6_lookup_store_pos.py', '.'), ('7_lookup_store_sc.py', '.'), ('8_count_sc_pos_scanner_model.py', '.'), ('POS_Model.csv', '.'), ('SC_Model.csv', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HardwareCapacity',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
