#!/bin/sh
set -eu

ln -svf /etc/monit/conf-available/openssh-server /etc/monit/conf-enabled
ln -svf /etc/monit/conf-available/rsyslog        /etc/monit/conf-enabled

ln -svf /srv/home/uwscli/etc/monit/conf/docker /etc/monit/conf-enabled

#~ /etc/init.d/monit start
#~ exit 0

/usr/bin/monit -c /etc/monit/monitrc -t

exec /usr/bin/monit -c /etc/monit/monitrc -l /run/uwscli/syslog/monit.log -I
