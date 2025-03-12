# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files


# Get all opus related libraries and data files
collected_opus_libs = collect_dynamic_libs('opuslib_next')
opus_datas = collect_data_files('opuslib_next')

print("Collected opus libs:", collected_opus_libs)
print("Collected opus datas:", opus_datas)

# Define all possible Opus library locations and their target names
opus_mappings = [
    ('/opt/homebrew/Caskroom/miniconda/base/envs/my_xiaozhi/lib/libopus.dylib', 'libopus.dylib'),
    ('/opt/homebrew/Caskroom/miniconda/base/envs/my_xiaozhi/lib/libopus.0.dylib', 'libopus.0.dylib'),
    ('/opt/homebrew/opt/opus/lib/libopus.dylib', 'libopus.dylib'),
    ('/opt/homebrew/lib/libopus.dylib', 'libopus.dylib'),
    ('/usr/local/lib/libopus.dylib', 'libopus.dylib'),
]

# Add all existing opus libraries to binaries with their target names
opus_binaries = []
for source_path, target_name in opus_mappings:
    if os.path.exists(source_path):
        print(f"Found opus library at: {source_path} -> {target_name}")
        opus_binaries.append((source_path, '.'))

if not opus_binaries:
    print("Warning: No Opus libraries found!")
    sys.exit(1)

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=opus_binaries + collected_opus_libs,
    datas=[]+opus_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[
        'pyi_rth_opus_pre.py',
        'pyi_rth_opus.py',
    ],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
