# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['CleaningAssign_mac.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('zones.json', '.'),
        ('names.json', '.'),
        ('exclusions.json', '.'),
        ('settings', 'settings')
    ],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'json',
        'datetime',
        'random',
        'requests'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CleaningAssign_mac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# 맥용 앱 번들 생성
app = BUNDLE(
    exe,
    name='CleaningAssign.app',
    icon=None,
    bundle_identifier='com.cleaningassign.app',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSUIElement': '0',
    },
) 