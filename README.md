# Arty
Arty is an image viewer designed for the needs of Art Historians written in Python and using the Kivy package for its GUI.

It allows for organizing a collection of images, annotate their metadata, compare them and view them in detail.

The current version of the application was developed by Florian Rieder, Caroline Roxana Rohrbach and Paul Zignani under the direction of Davide Picca, during the spring semester 2021 at the University of Lausanne (CH).

## Features
- Organize a corpus of images. Every image file is in one folder on your computer.
- Annotate the metadata of an image (artist, title, datation, etc)
- Sort and filter your collection based on the images metadata.
- Compare up to 4 images at once.
- Export your corpus to Powerpoint, with automatic legend generation based on the images' metadata.

## Hardware Requirements
- RAM: at least 8 GB
- Storage space : 220 MB

## Installation
1. create a virtual environment:
```python -m venv venv```

2. activate the environment:

- on MacOS
```. venv/bin/activate```

- on Windows
```venv\Scripts\activate```

3. install dependencies :
```pip install -r requirements.txt```


To run the application, use `python main.py`

## Building the application
The Python application is frozen into an executable using the Pyinstaller package.

### Note
Pyinstaller is incapable of cross-compiling. It means that you can only build the app for the OS of the machine you're compiling it with.
For better compatibility, build with the oldest version of the OS you want to support.

### MacOS
1. Create a `main.spec` file at the root of this repository and paste the following content:

`main.spec`
```python
# -*- mode: python -*-

from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks

block_cipher = None

dependencies = get_deps_minimal(window=True, image=True, audio=None, camera=None, video=None)
dependencies['hiddenimports'] += ['plyer.platforms.macosx.filechooser']

added_files = [
    ('/path/to/this/repo/venv/lib/python3.9/site-packages/pptx/templates', 'pptx/templates')
]

a = Analysis(['main.py'],
             pathex=['/path/to/this/repo'],
             cipher=block_cipher,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             datas=added_files,
             **dependencies)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Arty',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('path/to/this/repo'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Arty')
app = BUNDLE(coll,
             name='Arty.app',
             icon='resources/icon.icns',
             bundle_identifier="com.visio-images.arty",
             info_plist={
                 'NSHighResolutionCapable': 'True',
                 'NSPrincipalClass': 'NSApplication',
                 'NSAppleScriptEnabled': False,
                 'CFBundleDocumentTypes': [
                    {
                        'CFBundleTypeExtensions': ['arty'],
                        'CFBundleTypeName': 'Arty Collection',
                        'CFBundleTypeIconFile': 'resources/icon.icns',
                        'LSHandlerRank': 'Owner',
                        'CFBundleTypeRole': 'Editor'
                    }
                ]
             })

```
2. Replace placeholders where appropriate with the path to this repository on your machine.
3. Run the command `. build.sh` to build the executable and installer package. (You can also use the command `pyinstaller main.spec` to build only the executable. The builds can be found in the `dist` folder.

### Windows
1. Create a `main.spec` file at the root of this repository and paste the following content:

`main.spec`
```python
# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None

added_files = [
    ('C:\\path\\to\\this\\repo\\venv\\Lib\\site-packages\\pptx\\templates\\default.pptx', 'pptx\\templates')
]

a = Analysis(['main.py'],
             pathex=['C:\\path\\to\\this\\repo'],
             binaries=[],
             datas=added_files,
             hiddenimports=["plyer.platforms.win.filechooser"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Arty',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources\\icon.ico')
coll = COLLECT(exe, Tree('C:\\path\\to\\this\\repo'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Arty')
```

2. Replace placeholders where appropriate with the path to this repository on your machine.
3. At this stage, you can build an executable with pyinstaller using the `pyinstaller main.spec`command.
4. To be able to also build an installer package for the application, you need to install [Inno Setup 6](https://jrsoftware.org/isinfo.php).
5. After Inno Setup is installed on your system, you can either create your own `winsetup.iss` Inno Setup installer script using their wizard, or copy ours and change the paths where appropriate.

`winsetup.iss`
```
#define MyAppName "Arty"
#define MyAppVersion "Beta-1.0"
#define MyAppPublisher "Florian Rieder, Paul Zignani, Caroline Roxana Rohrbach"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "Arty.exe"
#define MyAppAssocName MyAppName + " Collection"
#define MyAppAssocExt ".arty"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{07F606D5-BB0D-4D8D-AD21-6D6CA95F2C37}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\Path\to\this\repo\dist
OutputBaseFilename=Arty setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Path\to\this\repo\dist\Arty\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Path\to\this\repo\dist\Arty\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
```

6. Once the `winsetup.iss` script is ready, running the build script with `build.bat` in `cmd` should take care of the entire build process, generating a folder with the .exe and dependencies and an installer package in the `dist` folder.

## Testing
Use the command `python tests.py` to run unit tests. Individual tests can be placed in the `tests` folder and imported into `tests.py` to be included in the tests.

## Dependencies
- Python 3
- Kivy
- KivyMD
- Plyer
- Pillow (PIL)
- Pyinstaller
- Python-pptx
- dataclasses_json
- unidecode

Other tools:
- Inno Setup 6 (Windows build installer)

## Contributors
- Florian Rieder
- Caroline Roxana Rohrbach
- Paul Zignani
