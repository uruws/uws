#!/bin/sh
set -eu

uwsrun='sudo -n -u uws'

${uwsrun} make -C /srv/uws/deploy uwscli-setup-schroot
#~ ${uwsrun} make -C /srv/deploy/Buildpack bootstrap

exec /srv/home/uwscli/sbin/sshd_init.sh
