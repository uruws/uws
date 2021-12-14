#!/bin/sh
set -eu
ansible-lint -x 301
# TODO: ansible-lint ./kali/*.yaml
# TODO: ansible-lint ./rstudio/*.yaml
exit 0
