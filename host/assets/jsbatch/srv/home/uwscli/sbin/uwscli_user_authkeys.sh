#!/bin/sh
set -eu
umask 0027

homedir=${1:?'home dir?'}
username=${2:?'username?'}
keyid=${3:?'keyid?'}

install -v -d -o "${username}" -g "${username}" -m 0750 "${homedir}/.ssh"

akfn="${homedir}/.ssh/authorized_keys"
ssh-import-id-gh --output "${akfn}" "${keyid}"

install -v -d -o "${username}" -g "${username}" -m 0600 "${akfn}"
exit 0
