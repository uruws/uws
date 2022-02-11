#!/bin/sh
set -eu
workdir=${1:?'workdir?'}
/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --workdir "${workdir}"
exec git -C "${workdir}" fetch --prune --prune-tags --tags
