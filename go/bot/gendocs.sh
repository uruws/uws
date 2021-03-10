#!/bin/sh
set -eu
echo 'uwsbot docs - monitoring bots engine'
fgrep -h '//uwsdoc:' ./go/bot/*.go | sed 's#\t//uwsdoc: ##' | sed 's/^-----$//'
exit 0
