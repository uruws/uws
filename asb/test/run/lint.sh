#!/bin/sh
set -eu
ansible-lint
# TODO: ansible-lint ./kali/*.yaml
# TODO: ansible-lint ./rstudio/*.yaml
exit 0
