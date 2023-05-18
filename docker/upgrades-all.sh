#!/bin/sh
set -eu

# uws/base
./docker/upgrades.py -t uws/base

# uws/ansible
./docker/upgrades.py -t uws/ansible -U docker/asb
./docker/upgrades.py -t uws/ansible

exit 0
