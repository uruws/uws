#!/bin/sh
set -eux

umask 0027

workdir=${1:?'workdir?'}
uri=${2:?'repo uri?'}

uwsrun='sudo -n -u uws'

ls -ld /srv/deploy
ls -lha /srv/deploy

if ! test -d "${workdir}"; then
	${uwsrun} git clone "${uri}" "${workdir}"
fi

exit 0
