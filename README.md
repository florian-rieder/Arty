# Arty

# Installation

```
python -m venv venv

# on unix systems
. venv/bin/activate
# on windows
venv\Scripts\activate

pip install -r requirements.txt
```

To run the application, use `python main.py`

# Building the application
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

Then run the command `pyinstaller main.spec`


# Contributors
- Florian Rieder
- Caroline Roxana Rohrbach
- Paul Zignani