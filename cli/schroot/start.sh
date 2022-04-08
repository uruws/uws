#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

cleanup() {
	${schroot_sess} -- /etc/init.d/docker stop || true
	sleep 1
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot -c uwscli-${profile} -n ${sess} -b

${schroot_sess} -- /etc/init.d/docker start
sleep 1
${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/uws/deploy uwscli-setup-schroot
#~ ${schroot_sess} -- /usr/bin/sudo -n -u uws make -C /srv/deploy/Buildpack bootstrap

${schroot_sess} -- /srv/home/uwscli/sbin/sshd_init.sh

exit 0
