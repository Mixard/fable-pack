---
name: nuitka-windows-packaging
description: Use when packaging Python GUI apps into small, fast Windows installers with Nuitka standalone mode plus Inno Setup. Covers verified Nuitka flag recipes (anti-bloat, module exclusion, console-mode), 32-bit vs 64-bit size tradeoffs, dist slimming rules, DLL size analysis, Inno Setup LZMA2 template, and deprecated-flag gotchas.
---

# Nuitka Windows Packaging (Commercial-Grade)

Approach: **Nuitka standalone folder mode (dist) + Inno Setup packaging**. No single-file builds (slow startup, antivirus flags, missing-DLL failures), no stray console window.

## Flag Gotchas (version-specific)

- `--disable-console` is **deprecated**. Use `--windows-console-mode=disable`.
- Inno Setup: `ArchitecturesInstallIn64BitMode=x64` is deprecated; use `x64compatible` — and only for 64-bit builds. Omit the directive entirely for 32-bit builds.
- `wmic` is removed on Windows 11 22H2+; detect CPU cores with the `%NUMBER_OF_PROCESSORS%` env var in batch scripts (a failed probe leaves `--jobs=0` = single-threaded compile).
- Nuitka + MinGW fails on non-ASCII source paths: copy sources to an ASCII path and set `PYTHONIOENCODING=utf-8`.
- If `_nuitka_temp.exe` appears in dist, exclude it from the installer `[Files]`.
- Do not use UPX compression — it reliably triggers antivirus false positives.

## Nuitka Compile Recipes

### Tkinter app (lightest; expect 80-120 MB after optimization)

```batch
nuitka --standalone --windows-console-mode=disable ^
    --lto=yes ^
    --jobs=8 ^
    --enable-plugin=tk-inter ^
    --enable-plugin=anti-bloat ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    --nofollow-import-to=unittest,test,pytest,_pytest,doctest,pdb,pdbpp ^
    --nofollow-import-to=setuptools,pip,distutils,pkg_resources ^
    --nofollow-import-to=email.mime,http.server,xmlrpc,pydoc ^
    --python-flag=no_docstrings ^
    --output-dir=dist ^
    --windows-icon-from-ico=icon.ico ^
    --remove-output ^
    main.py
```

### PyQt5 / PySide2 app (expect 120-250 MB after optimization)

Same as above, but replace the tk-inter plugin line with:

```batch
    --enable-plugin=pyqt5 ^
    --nofollow-import-to=PyQt5.QtWebEngine,PyQt5.QtWebEngineWidgets ^
    --nofollow-import-to=PyQt5.Qt3D,PyQt5.QtCharts ^
    --include-qt-plugins=sensible,styles,platforms ^
```

### Safe module-exclusion list (verified in production; saves 30-50 MB)

```
unittest,test,pytest,_pytest,doctest,pdb,pdbpp,
setuptools,pip,distutils,pkg_resources,
email.mime,http.server,xmlrpc,pydoc
```

### 32-bit vs 64-bit

32-bit Python saves 20-30% total size (python3x.dll -15%, Qt5Core -37%, numpy -33%). Use 32-bit when the app stays under 2 GB RAM and does not process files over 2 GB. 32- and 64-bit Pythons coexist:

```bash
py -3.12-32 -m pip install -r requirements.txt
py -3.12-32 -m nuitka --standalone ...
```

## Dist Slimming (saves 15-30%)

Delete from the dist folder after compiling:

1. `*.pdb` debug symbols
2. `*.pyi` type stubs
3. `__pycache__/` directories
4. `test/` and `tests/` directories
5. `docs/`, `examples/`, `samples/`, `demo/` directories
6. `*.pyc` bytecode
7. In each `*.dist-info/`: delete only `RECORD`, `INSTALLER`, `direct_url.json`. **Keep `METADATA` and `entry_points.txt`** — `importlib.metadata` reads them at runtime; deleting them breaks plugin discovery.

Compact PowerShell version:

```powershell
param([string]$DistPath)
Get-ChildItem $DistPath -Recurse -Include *.pdb,*.pyi,*.pyc -File | Remove-Item -Force
Get-ChildItem $DistPath -Recurse -Directory |
  Where-Object { $_.Name -match '^(__pycache__|tests?|docs|examples|samples|demo)$' } |
  Remove-Item -Recurse -Force
Get-ChildItem $DistPath -Recurse -Directory -Filter "*.dist-info" | ForEach-Object {
  foreach ($f in "RECORD","INSTALLER","direct_url.json") {
    $p = Join-Path $_.FullName $f
    if (Test-Path $p) { Remove-Item $p -Force }
  }
}
```

## DLL Size Analysis

Sort `*.dll` in dist by size; typical heavy hitters and fixes (numbers from a production PySide2 + OpenCV + Playwright app, 323 MB total, 71 DLLs = 93 MB):

| DLL | Typical size | Fix |
| --- | --- | --- |
| libopenblas | ~27 MB | Only needed for heavy numeric work |
| opencv_videoio_ffmpeg | ~18 MB | Switch to `opencv-python-headless` |
| opengl32sw | ~15 MB | Software GL renderer; usually safe to delete (hardware rendering) |
| Qt5Core | ~5 MB | Exclude unused Qt modules (WebEngine, 3D, Charts) |
| mfc140 | ~5 MB | MFC dependency |
| d3dcompiler | ~3.5 MB | DirectX compiler |
| DLLs whose stem ends in `d` | varies | Debug builds — delete |
| vcruntime*/msvcp* | small | Required; keep |

## VC++ Runtime

Either compile with `--static-libpython=yes`, or bundle the redistributable in Inno Setup. **The redistributable architecture must match the Python/Nuitka build architecture** (x86 for 32-bit builds, x64 for 64-bit):

```iss
[Files]
Source: "{#MySourceDir}\..\vc_redist.x86.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "{tmp}\vc_redist.x86.exe"; Parameters: "/quiet /norestart"; Flags: waituntilterminated
```

Download: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

## Inno Setup Template (Inno Setup 6.x)

```iss
#define MyAppName        "AppName"
#define MyAppVersion     "1.0.0"
#define MyAppPublisher   "Publisher"
#define MyAppURL         "https://example.com"
#define MyAppExeName     "App.exe"
#define MySourceDir      "D:\project\dist\App.dist"
#define MyOutputDir      "D:\project\output"

[Setup]
AppId={{GENERATE-A-UNIQUE-GUID}}   ; Inno Setup: Tools > Generate GUID
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
PrivilegesRequired=admin
OutputDir={#MyOutputDir}
OutputBaseFilename=Setup_{#MyAppName}_v{#MyAppVersion}
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
; Maximum compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
; 64-bit builds ONLY (omit for 32-bit):
;ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[UninstallDelete]
Type: filesandordirs; Name: "{app}\*"

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
```

## Expected Results (measured)

| Optimization | Size reduction | Startup gain |
|---|---|---|
| `--lto=yes` | 5-10% | 10-20% |
| anti-bloat plugin | 15-25% | - |
| module exclusion | 20-35% | ~5% |
| dist slimming | 25-40% | - |
| 32-bit build | 40-60% | - |
| All combined | 45-65% | 15-25% |

## Troubleshooting

- **Missing python3xx.dll after install**: must use `--standalone`; verify the DLL exists in dist; never ship single-file mode.
- **App does nothing on launch**: heavy imports can block GUI startup on clean machines; defer heavy imports until first use and add logging. Also run the exe from CMD to see errors and check the VC++ runtime.
- **SmartScreen / antivirus warnings**: code-sign the installer (EV cert gets immediate trust; standard certs accrue reputation); submit to AV vendors for allow-listing; never use UPX.
