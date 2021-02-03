#!/bin/sh
set -eu

DIST=${1:?'dist name?'}
SECT=${2:-'main contrib non-free'}

SLF=/etc/apt/sources.list.d/${DIST}.list

echo "deb http://deb.debian.org/debian/ ${DIST} ${SECT}" >${SLF}

export DEBIAN_FRONTEND=noninteractive

apt-get clean
apt-get update
apt-get dist-upgrade -yy --purge

apt-get clean
apt-get autoremove -yy --purge
rm -rf /var/lib/apt/lists/* \
	/var/cache/apt/archives/*.deb \
	/var/cache/apt/*cache.bin

exit 0
