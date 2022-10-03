#!/bin/sh
set -eu

ln -svf /etc/monit/conf-available/openssh-server /etc/monit/conf-enabled

ln -svf /srv/home/uwscli/etc/monit/conf/docker /etc/monit/conf-enabled

exec /usr/bin/monit -I -c /etc/monit/monitrc
