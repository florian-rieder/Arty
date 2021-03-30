# Arty

# Installation

1. create a virtual environment:
```python -m venv venv```

2. activate the environment:

- on unix
```. venv/bin/activate```

- on windows
```venv\Scripts\activate```

3. install dependencies :
```pip install -r requirements.txt```


To run the application, use `python main.py`

# Building the application
1. Create a `main.spec` file at the root of this repository and paste the appropriate content depending on your OS.
2. Replace the `pathex` in the `Analysis` part of the spec file with the path to this repository on your machine.
3. Then run the command `pyinstaller main.spec` to build the executable.

## MacOS
`main.spec`
```
# -*- mode: python -*-

block_cipher = None
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

a = Analysis(['main.py'],
             pathex=['/path/to/this/repo'],
             cipher=block_cipher,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             **get_deps_all())
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
coll = COLLECT(exe, Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Arty')
app = BUNDLE(coll,
             name='Arty.app',
             icon=None,
         bundle_identifier=None)
```

## Windows
`main.spec`
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from kivy_deps import sdl2, glew

a = Analysis(['main.py'],
             pathex=['C:\\path\\to\\this\\repo'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          console=True )
coll = COLLECT(exe, Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='Arty')
```

## Note
Pyinstaller is incapable of cross-compiling. It means that you can only build the app for the OS of the machine you're compiling it with.
For better compatibility, build with the oldest version of the OS you want to support.

# Unit testing
Use the command `python -m tests.Tests` to run unit tests.

# Contributors
- Florian Rieder
- Caroline Roxana Rohrbach
- Paul Zignani