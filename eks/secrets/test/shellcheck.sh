#!/bin/sh
set -eu
shellcheck --exclude=SC1090 ./eks/secrets/*.sh
exit 0
