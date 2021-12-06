#!/bin/sh
set -eu
make clean
make prune
nice ionice make bootstrap
nice ionice make eks
make prune
make clean
exit 0
