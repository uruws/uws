#!/bin/sh
set -eu

buildd=${PWD}/srv/munin/build
mkdir -vp ${buildd}
install -v -C ${PWD}/python/lib/sendmail.py ${buildd}/sendmail.py

# munin
docker build $@ --rm -t uws/munin \
	-f srv/munin/Dockerfile \
	./srv/munin
# munin-2203
docker build $@ --rm -t uws/munin-2203 \
	-f srv/munin/Dockerfile.2203 \
	./srv/munin

exit 0
