#!/bin/sh
set -eu

umask 0027

uri=${1:?'uri?'}
workdir=${2:?'workdir?'}

if ! test -d "${workdir}"; then
	git clone --depth 15 "${uri}" "${workdir}"
fi

exit 0
