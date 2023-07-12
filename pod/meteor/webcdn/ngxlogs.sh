#!/bin/sh
set -eu
exec ~/pod/lib/ngxlogs.py "$@" meteor/webcdn
