#!/bin/sh
set -eu

app=${1:?'app?'}

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${app}"

docker images | grep -F "${app}" |
	awk '{ print $1":"$2 }' | xargs docker rmi

exit 0
