#!/bin/bash

#aarch64 strace compiling
git clone git@github.com:strace/strace.git
echo "Entering into strace dir..."
cd strace
echo "Set aaarch64 compiler"
export CC=/usr/bin/aarch64-linux-gnu-gcc
echo "Export stati C compile flags..."
export CFLAGS="-O2 -static"
echo "export LDFLAGS"
export LDFLAGS="-static -pthread"
echo "Precompiling steps..."
libtoolize --force
aclocal
autoheader
autoconf
./bootstrap
./configure --host=aarch64-linux --enable-mpers=no
echo "Starting compile process..."
make -j4
echo "Saving compiled strace to /tools/strace/"
make install DESTDIR=../../../tools/strace/
echo "Removing strace source code..."
cd ..
rm -r strace/
echo "Done!"
echo "Extracting strace executable..."
cd ../../
cp ./tools/strace/usr/local/bin/strace ./tools/strace/strace
#rm -r ./tools/strace/usr/
echo "Done!"
