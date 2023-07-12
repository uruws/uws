#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get clean
exec apt-get update
