#!/bin/sh
set -eu

profile=${1:?'profile?'}
service=${2:?'service?'}

if ! test -d /etc/schroot/uwscli-${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}-${service}"

cleanup() {
	schroot -c ${sess} -e
}

schroot -c uwscli-${profile} -n ${sess} -b

trap cleanup INT EXIT

schroot_cmd="schroot -c ${sess} -d /root -u root -r"

${schroot_cmd} -- install -v -d -o root -g uwscli -m 0750 /etc/uws/cli
${schroot_cmd} -- install -v -C -o root -g uwscli -m 0640 \
	/usr/local/etc/local_conf.py \
	/etc/uws/cli/local_conf.py

${schroot_cmd} -- /srv/home/uwscli/sbin/${service}_init.sh

exit 0
