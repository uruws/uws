#!/bin/sh
set -eu

doas install -v -m 0440 -o root -g root \
	./host/assets/jsbatch/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

doas install -v -d -m 0750 -o uws -g uws /home/uws

doas /usr/sbin/adduser uws ${SCHROOT_GROUP}
doas /usr/sbin/adduser uws docker

PATH=/srv/home/uwscli/bin:${PATH}
exec /bin/bash -i
