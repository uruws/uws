#!/bin/sh
set -eu

profile=${1:?'profile?'}
service=${2:?'service?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
if test 'Xsshd' != "X${service}"; then
	sess="uwscli-${profile}-${service}"
fi

schroot_sess="schroot -c ${sess} -d /root -u root -r"

cleanup() {
	if test 'Xsshd' = "X${service}"; then
		${schroot_sess} -- /etc/init.d/docker stop || true
	fi
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot -c uwscli-${profile} -n ${sess} -b

if test 'Xsshd' = "X${service}"; then
	${schroot_sess} -- /etc/init.d/docker start
	${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/uws/deploy uwscli-setup-schroot
	#~ ${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/deploy/Buildpack bootstrap
fi

${schroot_sess} -- /srv/home/uwscli/sbin/${service}_init.sh

exit 0
