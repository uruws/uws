#!/bin/sh
set -eu

app=${1:?'app?'}

docker images | grep -F "${app}" |
	awk '{ print $1":"$2 }' | xargs docker rmi

exit 0
