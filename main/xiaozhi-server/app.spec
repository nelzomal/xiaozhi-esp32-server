# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, collect_submodules
import shutil
from funasr.register import tables
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Get all opus related libraries and data files
collected_opus_libs = collect_dynamic_libs('opuslib_next')
opus_datas = collect_data_files('opuslib_next')

# Get all funasr related files
funasr_datas = collect_data_files('funasr')
funasr_imports = collect_submodules('funasr')

print("Collected opus libs:", collected_opus_libs)
print("Collected opus datas:", opus_datas)
print("Collected funasr datas:", funasr_datas)

# Define all possible Opus library locations and their target names
opus_mappings = [
    ('/opt/homebrew/Caskroom/miniconda/base/envs/xiaozhi-esp32-server/lib/libopus.dylib', 'libopus.dylib'),
    ('/opt/homebrew/Caskroom/miniconda/base/envs/xiaozhi-esp32-server/lib/libopus.0.dylib', 'libopus.0.dylib'),
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

# Get ASR model and config files
asr_files = []
asr_model_dir = 'models/SenseVoiceSmall'  # Updated path
if os.path.exists(asr_model_dir):
    print(f"Found ASR model directory: {asr_model_dir}")
    for root, dirs, files in os.walk(asr_model_dir):
        for file in files:
            full_path = os.path.join(root, file)
            # Keep the models directory structure
            rel_path = os.path.dirname(os.path.relpath(full_path, '.'))
            print(f"Adding ASR file: {full_path} -> {rel_path}")
            asr_files.append((full_path, rel_path))
else:
    print(f"Warning: ASR model directory not found at {asr_model_dir}")

# Get FunASR source files path
funasr_base_path = '/opt/homebrew/Caskroom/miniconda/base/envs/xiaozhi-esp32-server/lib/python3.10/site-packages/funasr'

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=opus_binaries + collected_opus_libs,
    datas=[
        # Copy config.yaml to root directory
        ('config.yaml', '.'),
        # Add ASR related files
        ('core/providers/asr/fun_local.py', 'core/providers/asr'),
        # Add LLM related files
        ('core/providers/llm', 'core/providers/llm'),
        # Add TTS related files
        ('core/providers/tts', 'core/providers/tts'),
        # Add Memory related files
        ('core/providers/memory', 'core/providers/memory'),
        # Add Intent related files
        ('core/providers/intent', 'core/providers/intent'),
        # Add source files for inspection
        (os.path.join(funasr_base_path, 'models/sense_voice/model.py'), 'funasr/models/sense_voice'),
        (os.path.join(funasr_base_path, 'models/specaug/specaug.py'), 'funasr/models/specaug'),
    ] + opus_datas + asr_files + funasr_datas,
    hiddenimports=[
        # Add ASR related imports
        'core.providers.asr.fun_local',
        'funasr',
        # Add LLM related imports
        'core.providers.llm',
        'core.utils.llm',
        # Add OpenAI package
        'openai',
        'openai.api_resources',
        'openai.api_resources.abstract',
        # Add TTS related imports
        'core.providers.tts',
        'core.utils.tts',
        # Add edge-tts package
        'edge_tts',
        'edge_tts.exceptions',
        'edge_tts.communicate',
        # Add Memory related imports
        'core.providers.memory',
        'core.utils.memory',
        # Add Intent related imports
        'core.providers.intent',
        'core.utils.intent',
        'funasr.models.sense_voice.model',
        'funasr.models.specaug.specaug',
    ] + funasr_imports + collect_submodules('funasr'),
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[
        'pyi_rth_opus_pre.py',
        'pyi_rth_opus.py', 
    ],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# Add runtime environment variables
a.environ = {
    'DYLD_LIBRARY_PATH': sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd(),
    'LD_LIBRARY_PATH': sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd(),
    'DYLD_FALLBACK_LIBRARY_PATH': sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd()
}

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)