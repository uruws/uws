#!/bin/sh
set -eux

umask 0027

workdir=${1:?'workdir?'}
uri=${2:?'repo uri?'}

uwsrun='sudo -n -u uws'

if test -d "${workdir}"; then
	${uwsrun} git -C "${workdir}" pull --no-rebase || true
else
	${uwsrun} git clone "${uri}" "${workdir}"
fi

exit 0
