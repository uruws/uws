#!/bin/sh
set -eu

umask 0027

# shellcheck disable=SC2048
for username in $*; do
	chmod -v 0750 "~${username}"
	install -v -C -m 0644 ~uwscli/etc/user.bash_profile \
		"~${username}/.bash_profile"
done

exit 0
