#!/bin/sh
set -eu
exec ansible-playbook -i ${ANSIBLE_INVENTORY} $@
