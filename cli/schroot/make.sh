#!/bin/sh
set -eu

profile=${1:?'profile?'}
repo=${2:?'repo?'}
target=${3:?'target?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

sess="uwscli-${profile}"
schroot_sess="schroot -c ${sess} -d /root -u root -r"

${schroot_sess} -- /usr/bin/true || {
	exit 2
}
${schroot_sess} -- /usr/bin/test -d /srv/deploy/${repo} || {
	echo "invalid repository: ${repo}" >&2
	exit 3
}

exec ${schroot_sess} -- /usr/bin/make -C /srv/deploy/${repo} ${target}
