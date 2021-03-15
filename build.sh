#!bin/bash

# pyinstaller doesn't do cross compile, so we have to build on Windows/Mac separately
# --noconsole to get rid of the console
# --debug all|imports to enable debugging in the console

ENTRYPOINT="main"
SPECFILE="$ENTRYPOINT.spec"
PYFILE="$ENTRYPOINT.py"

if [ -f "$SPECFILE" ]; then
  #if there is a spec file, compile from it
  pyinstaller $SPECFILE
elif [ -f "$PYFILE" ]; then
  #else, compile from the entrypoint python script
  pyinstaller \
    --paths=venv/lib/python3.8/site-packages \
    --add-data=templates:templates \
    --add-data=static:static \
    --noconsole \
    $PYFILE
fi


