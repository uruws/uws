#!/bin/sh
set -eu

if test -s /var/log/docker.log; then
	mv -vf /var/log/docker.log /var/log/docker.log.1
fi

echo 'export DOCKER_RAMDISK=true' >/etc/default/docker

ln -svf /srv/home/uwscli/etc/monit/conf/docker /etc/monit/conf-enabled

/etc/init.d/docker start

exit 0
