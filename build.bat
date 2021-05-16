@echo off
Rem ###              Building script for Arty on Windows                ###

echo [BUILD] Removing dist and build folders...

Rem Removing the dist and build folders, because they can cause problem.
Rem The pyinstaller --clean option doesn't seem to help.

rmdir /s /q .\dist
rmdir /s /q .\build


echo [BUILD] Starting the building process...

pyinstaller main.spec


echo [BUILD] Creating installer...

Rem Here we create an installer package (using Inno Setup 6)
Rem See: https://jrsoftware.org/isinfo.php

"C:/Program Files (x86)/Inno Setup 6/ISCC.exe" winsetup.iss


echo [BUILD] Build complete !
echo         Files are in the 'dist' folder
