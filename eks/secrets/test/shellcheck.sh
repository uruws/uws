#!/bin/sh
set -eu
shellcheck ./eks/secrets/test/*.sh
shellcheck --exclude=SC1090 ./eks/secrets/*.sh
exit 0
