#!/bin/sh
set -eu
# herokud
docker build --rm -t uws/herokud \
	./srv/herokud
exit 0
