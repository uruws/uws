#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/munin-node ./srv/munin-node
