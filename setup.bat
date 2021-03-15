# setup virtual environment
python -m venv venv

# set execution policy of powershell so you can execute the activation script
Set-ExecutionPolicy Unrestrictede -Force

# activate environment
venv\Scripts\activate

# install dependencies
pip install \
    flask \
    PyQt5==5.15.0 \
    PyQtWebEngine==5.15.0 \
    git+git://github.com/widdershin/flask-desktop.git \
    pyinstaller

echo "To activate the virtual environment next time, use: \nvenv\Scripts\activate"