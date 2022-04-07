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

exit 0
