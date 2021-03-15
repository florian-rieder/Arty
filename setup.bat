Rem setup virtual environment
python -m venv venv

Rem set execution policy of powershell so you can execute the activation script
Set-ExecutionPolicy Unrestricted -Force

Rem activate environment
venv\Scripts\activate

Rem install dependencies
pip install \
    flask \
    PyQt5==5.15.0 \
    PyQtWebEngine==5.15.0 \
    git+git://github.com/widdershin/flask-desktop.git \
    pyinstaller

echo "To activate the virtual environment, use: \nvenv\Scripts\activate"