#!/bin/sh
hostip=$(ip addr show docker0 | grep -Po 'inet \K[\d.]+')
if test -n "${hostip}"; then
	echo ${hostip}
else
	# safe(?) fallback
	echo 127.0.0.1
fi
exit 0
