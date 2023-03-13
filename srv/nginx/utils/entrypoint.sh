#!/bin/sh
set -eu

echo "nginx: start $(date -R)"

ln -svf /dev/stderr /var/log/nginx/access_log
ln -svf /dev/stderr /var/log/nginx/error_log

/usr/sbin/nginx -t
exec /usr/sbin/nginx -g 'daemon off;'
