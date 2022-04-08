#!/bin/sh
set -eu

profile=${1:?'profile?'}
repo=${2:?'repo?'}
target=${3:?'target?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

if ! test -d /srv/uwscli/${profile}/deploy/${repo}; then
	echo "invalid repository: ${repo}" >&2
	exit 2
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

exec ${schroot_sess} -- /usr/bin/make -C /srv/deploy/${repo} ${target}
