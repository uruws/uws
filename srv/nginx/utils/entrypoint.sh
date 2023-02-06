#!/bin/sh
set -eu
/usr/bin/nginx -t
exec /usr/bin/nginx
