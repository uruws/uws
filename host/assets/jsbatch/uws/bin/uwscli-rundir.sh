#!/bin/sh
set -eu

umask 0027

install -v -d -o uws -g uwscli -m 0750 /run/uwscli
install -v -d -o uws -g uwscli -m 0770 /run/uwscli/nq
install -v -d -o uws -g uwscli -m 0770 /run/uwscli/build
install -v -d -o uws -g uwscli -m 0770 /run/uwscli/logs

exit 0
