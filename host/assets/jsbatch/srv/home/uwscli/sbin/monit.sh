#!/bin/sh
set -eu
/usr/bin/monit -c /etc/monit/monitrc -t
exec /usr/bin/monit -c /etc/monit/monitrc -I
