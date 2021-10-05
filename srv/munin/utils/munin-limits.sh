#!/bin/sh
set -eu
sleep 60
exec /usr/share/munin/munin-limits --force --contact alerts
