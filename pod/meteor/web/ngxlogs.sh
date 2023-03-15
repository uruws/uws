#!/bin/sh
set -eu
exec ~/pod/lib/ngxlogs.py "$@" meteor/web/gw
