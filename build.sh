#!/bin/bash

echo "[BUILD] Removing dist and build folders..."
# removing the dist and build folders if they exist, because they cause
# problems with the build process, that the --clean pyinstaller argument
rm -rf ./dist ./build

echo "[BUILD] Starting the building process..."
pyinstaller main.spec

echo "[BUILD] Build complete !"