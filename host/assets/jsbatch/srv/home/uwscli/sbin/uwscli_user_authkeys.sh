#!/bin/sh
set -eu
umask 0027

homedir=${1:?'home dir?'}
username=${2:?'username?'}
keyid=${3:?'keyid?'}

akfn="${homedir}/.ssh/authorized_keys"

install -v -d -o "${username}" -g "${username}" -m 0550 "${homedir}/.ssh"

ssh-import-id --output "${akfn}".new "gh:${keyid}"

install -v -C -o "${username}" -g "${username}" -m 0400 "${akfn}".new "${akfn}"

rm -f "${akfn}".new
exit 0
