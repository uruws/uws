#!/bin/sh
set -eu

app=${1:?'app?'}
version=${2:?'version?'}

docker images |
	grep -F "${app}" |
	grep -F "${version}" |
	awk '{ print $1":"$2 }' |
	xargs docker rmi

exit 0
