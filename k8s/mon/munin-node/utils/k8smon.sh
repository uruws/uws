#!/bin/sh
set -eu
plname=$(basename "${0}" | tr -s '_' '/')
base_uri='http://cluster.mon:2800'
action='report'
if test 'Xconfig' = "X${1:-''}"; then
	action='config'
fi
uri="${base_uri}/${action}/${plname}"
exec wget -q -O - "${uri}"
