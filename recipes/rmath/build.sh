#!/bin/bash

set -e # Stop on any error
export LIBnn=lib

echo "Configuring..." # Configure with verbose output
./configure \
    --prefix="${PREFIX}" \
    --enable-lto=yes \
    --enable-R-profiling=no \
    --enable-byte-compiled-packages=no \
    --enable-java=no \
    --enable-nls=no \
    --enable-openmp=no \
    --enable-rpath=no \
    --with-aqua=no \
    --with-cairo=no \
    --with-ICU=no \
    --with-internal-tzcode=yes \
    --with-jpeglib=no \
    --without-libintl-prefix \
    --with-libpng=no \
    --with-libtiff=no \
    --with-readline=no \
    --with-recommended-packages=no \
    --with-tcltk=no \
    --with-x=no || { echo "Configuration failed"; exit 1; }

echo "Entering src/nmath/standalone directory..."
pushd src/nmath/standalone || { echo "Failed to enter src/nmath/standalone directory"; exit 1; }

# Determine number of cores for make command differently based on OS
if [[ $(uname) == "Darwin" ]]; then
    NUM_CORES=$(sysctl -n hw.ncpu)
else
    NUM_CORES=$(nproc)
fi

echo "Building with ${NUM_CORES} cores..."
make --jobs="${NUM_CORES}" shared || { echo "Make failed"; exit 1; }
echo "Installing..."
make install || { echo "Make install failed"; exit 1; }

find "${PREFIX}" || { echo "Find command failed"; exit 1; }

echo "Exiting src/nmath/standalone directory..."
popd || exit

echo "Build script completed successfully."