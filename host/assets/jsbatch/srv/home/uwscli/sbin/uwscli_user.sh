#!/bin/sh
set -eux

umask 0027

homedir=${1:?'home dir?'}
userid=${2:?'user ID?'}
username=${3:?'username?'}

groupadd -g "${userid}" "${username}" || true

create_home='-m'
if test -d "${homedir}/${username}"; then
	create_home='-M'
fi

useradd -d "${homedir}/${username}" "${create_home}" \
	-c "${username}" \
	-g "${userid}" \
	-u "${userid}" \
	-s /bin/bash \
	"${username}" || true

chmod -v 0750 "${homedir}/${username}"

install -v -C -o root -g "${username}" -m 0640 \
	~uwscli/etc/user.bash_profile "${homedir}/${username}/.bash_profile"

exit 0
