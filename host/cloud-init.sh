#!/bin/sh
set -eu
st=$(cloud-init status)
if test "X${st}" != 'Xstatus: done'; then
	echo "cloud-init invalid status: ${st}" >&2
	exit 1
fi
cloud-init clean
cloud-init init --local
cloud-init modules --mode config
cloud-init modules --mode final
exit 0
