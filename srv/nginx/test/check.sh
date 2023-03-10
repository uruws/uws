#!/bin/sh
set -eu

# setup

rm -f /etc/nginx/uws-sites-enabled/*

ln -sf /dev/stderr /var/log/nginx/access_log
ln -sf /dev/stderr /var/log/nginx/error_log

# test default

/usr/sbin/nginx -t

# test proxy

install -v -m 644 /root/test/site/proxy /etc/nginx/uws-sites-enabled

/usr/sbin/nginx -t

rm -f /etc/nginx/uws-sites-enabled/*

# test upstream-json-logs

install -v -m 644 /root/test/site/upstream-json-logs /etc/nginx/uws-sites-enabled

/usr/sbin/nginx -t

rm -f /etc/nginx/uws-sites-enabled/*

exit 0
