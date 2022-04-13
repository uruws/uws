#!/bin/sh
set -eu
umask 0027

homedir=${1:?'home dir?'}
username=${2:?'username?'}
keyid=${3:?'keyid?'}

install -v -d -o "${username}" -g "${username}" -m 0550 "${homedir}/.ssh"

akfn="${homedir}/.ssh/authorized_keys"
ssh-import-id --output "${akfn}" "gh:${keyid}"

chown -v "${username}:${username}" "${akfn}"
chmod -v 0400 "${akfn}"

exit 0
