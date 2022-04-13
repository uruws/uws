#!/bin/sh
set -eu
umask 0027

homedir=${1:?'home dir?'}
username=${2:?'username?'}
keyid=${3:?'keyid?'}

akfn="${homedir}/${username}/.ssh/authorized_keys"

install -v -d -o "${username}" -g "${username}" -m 0750 "${homedir}/${username}/.ssh"

rm -f "${akfn}.new"
ssh-import-id --output "${akfn}.new" "gh:${keyid}"
cat /srv/uwscli/test/secret/ssh/id_ed25519.pub >>"${akfn}.new"

install -v -C -o "${username}" -g "${username}" -m 0400 "${akfn}.new" "${akfn}"

rm -f "${akfn}.new"
exit 0
