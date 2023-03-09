#!/bin/sh
set -eu

# setup

rm -vf /etc/nginx/uws-sites-enabled/*

ln -svf /dev/stderr /var/log/nginx/access_log
ln -svf /dev/stderr /var/log/nginx/error_log

# test default

/usr/sbin/nginx -t

# test proxy

install -v -m 644 /root/test/site/proxy /etc/nginx/uws-sites-enabled

/usr/sbin/nginx -t

rm -vf /etc/nginx/uws-sites-enabled/*

exit 0
