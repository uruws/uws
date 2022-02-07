#!/bin/sh
set -eu

doas install -v -m 0440 -o root -g root \
	./host/assets/jsbatch/etc/sudoers.d/99-uwscli \
	/etc/sudoers.d/99-uwscli

PATH=/srv/home/uwscli/bin:${PATH}
exec /bin/bash -i
