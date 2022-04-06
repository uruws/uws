#!/bin/sh
set -eu
install -v -d -o root -g root -m 0755 /run/sshd
exec /usr/sbin/sshd -D -e -4 -q
