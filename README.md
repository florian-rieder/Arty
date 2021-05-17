# Arty
Arty is an image viewer designed for the needs of Art Historians.

# Installation

1. create a virtual environment:
```python -m venv venv```

2. activate the environment:

- on MacOS
```. venv/bin/activate```

- on windows
```venv\Scripts\activate```

3. install dependencies :
```pip install -r requirements.txt```


To run the application, use `python main.py`

# Building the application
1. Create a `main.spec` file at the root of this repository and paste the appropriate content depending on your OS.
2. Replace placeholders where appropriate with the path to this repository on your machine.
3. Then run the command `pyinstaller main.spec` to build the executable.

### Note
Pyinstaller is incapable of cross-compiling. It means that you can only build the app for the OS of the machine you're compiling it with.
For better compatibility, build with the oldest version of the OS you want to support.

## MacOS
`main.spec`
```
# -*- mode: python -*-

block_cipher = None

from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks

dependencies = get_deps_minimal(window=True, image=True, audio=None, camera=None, video=None)
dependencies['hiddenimports'] += ["plyer.platforms.macosx.filechooser"]

a = Analysis(['main.py'],
             pathex=['/path/to/this/repo'],
             cipher=block_cipher,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
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

Once the main.spec file is created, running the build script with `. build.sh` should take care of the entire build process, generating a MacOSX application and an installer package in the `dist` folder.

## Windows
`main.spec`
```
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

Once the main.spec file is created, you can build an executable of Arty. The build script for Windows requires an extra installation step to be able to generate an installer package. The software [Inno Setup 6](https://jrsoftware.org/isinfo.php) is used. You then generate a winsetup.iss file and run the build script with `build.bat` in `cmd` should take care of the entire build process, generating a folder with the .exe and dependencies and an installer package in the `dist` folder.

# Unit testing
Use the command `python -m tests.Tests` to run unit tests.

# Dependencies
- Python 3
- Kivy
- Plyer
- Pillow
- Pyinstaller
- Python-pptx
- dataclasses_json
- unidecode

Other tool:
- Inno Setup 6 (Windows build installer)

# Contributors
- Florian Rieder
- Caroline Roxana Rohrbach
- Paul Zignani