#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/munin-backend ./srv/munin-backend
