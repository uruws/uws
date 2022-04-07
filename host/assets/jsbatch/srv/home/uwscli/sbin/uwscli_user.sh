#!/bin/sh
set -eu

umask 0027

homedir=${1:?'home dir?'}
userid=${2:?'user ID?'}
username=${3:?'username?'}

groupadd -o -g "${userid}" "${username}" || true

useradd -o -d "${homedir}/${username}" -m -c "${username}" -s /bin/bash \
	-g "${userid}" -u "${userid}" "${username}" || true

chmod -v 0750 "${homedir}/${username}"

install -v -C -o root -g "${username}" -m 0640 \
	~uwscli/etc/user.bash_profile "${homedir}/${username}/.bash_profile"

exit 0
