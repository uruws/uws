#!/bin/sh
set -eu

uwsrun='sudo -n -u uws'

${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot

exec /srv/home/uwscli/sbin/sshd_init.sh
