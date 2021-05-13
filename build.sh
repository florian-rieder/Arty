#!/bin/bash

echo "[BUILD] Removing dist and build folders..."
# removing the dist and build folders if they exist, because they cause
# problems with the build process, that the --clean pyinstaller argument
# doesn't seem to solve.
rm -rf ./dist ./build

echo "[BUILD] Starting the building process..."
pyinstaller main.spec

echo "[BUILD] Creating pkg..."
pkgbuild --install-location /Applications --component ./dist/Arty.app ./dist/Arty.pkg

echo "[BUILD] Build complete !"