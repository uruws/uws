#!/bin/sh
set -eu

# uws/base
./docker/upgrades.py -t uws/base

# uws/awscli
./docker/upgrades.py -t uws/awscli

# uws/ansible
./docker/upgrades.py -t uws/ansible -U docker/asb
./docker/upgrades.py -t uws/ansible

# uws/golang
./docker/upgrades.py -t uws/golang -U docker/golang
./docker/upgrades.py -t uws/golang

# uws/python
./docker/upgrades.py -t uws/python -U docker/python
./docker/upgrades.py -t uws/python

# uws/mkcert
./docker/upgrades.py -t uws/mkcert -U docker/mkcert
./docker/upgrades.py -t uws/mkcert

exit 0
