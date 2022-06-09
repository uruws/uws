#!/bin/sh
set -eu

app=${1:?'app name?'}
version=${2:?'version?'}

export UWSCLI_LOG=on
export UWSCLI_DEBUG=on

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${app}" --ops deploy

/srv/home/uwscli/bin/app-autobuild --deploy "${app}" "${version}"

exit 0
