#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get clean
apt-get update
apt-get dist-upgrade -yy --purge
apt-get clean
apt-get autoremove -yy --purge
exit 0
