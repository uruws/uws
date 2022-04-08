#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}-build"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

cleanup() {
	${schroot_sess} -- /etc/init.d/docker stop
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot -c uwscli-${profile} -n ${sess} -b

${schroot_sess} -- /etc/init.d/docker start
${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/uws/deploy uwscli-setup-schroot
#~ ${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/deploy/Buildpack bootstrap

exit 0
