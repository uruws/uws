#!/bin/sh
set -eu
echo 'uwsbot docs - monitoring bots engine'
fgrep -h '//uwsdoc:' *.go | sed 's#//uwsdoc: ##'
exit 0
