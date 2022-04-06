#!/bin/sh
set -eu

umask 0027

homedir=${1:?'home dir?'}
username=${2:?'username?'}
userid=${3:?'user ID?'}

groupadd -o -g "${userid}" "${username}"

useradd -o -d "${homedir}/${username}" -m -c "${username}" -s /bin/bash \
	-g "${userid}" -u "${userid}" "${username}"

chmod -v 0750 "${homedir}/${username}"

exit 0
