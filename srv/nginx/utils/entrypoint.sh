#!/bin/sh
set -eu

echo "nginx: start $(date '+%d/%b/%Y:%H:%M:%S')"

ln -svf /dev/stderr /var/log/nginx/access_log
ln -svf /dev/stderr /var/log/nginx/error_log

/usr/sbin/nginx -t
exec /usr/sbin/nginx -g 'daemon off;'
