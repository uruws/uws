#!/bin/sh
set -eu
make clean
make prune
make bootstrap
make eks
make prune
make clean
exit 0
