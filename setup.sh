#!bin/bash

# setup virtual environment
python -m venv venv
# activate environment
. venv/bin/activate

# install dependencies
pip install \
    flask \
    PyQt5==5.15.0 \
    PyQtWebEngine==5.15.0 \
    git+git://github.com/widdershin/flask-desktop.git \
    pyinstaller

echo "To activate the virtual environment next time, use: \n. venv/bin/activate"