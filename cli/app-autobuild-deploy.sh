#!/bin/sh
set -eu

app=${1:?'app name?'}
version=${2:?'version?'}

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --ops "${app}"

/srv/home/uwscli/bin/app-autobuild --deploy "${app}" "${version}"

exit 0
