#!/bin/sh
set -eu
name=${1:?'key name?'}
exec uwskube get secret "uwsefs-cfg-${name}" \
	-o jsonpath="{.data['value']}" |
	base64 -d
