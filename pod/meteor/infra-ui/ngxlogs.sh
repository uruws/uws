#!/bin/sh
set -eu
exec ~/pod/lib/ngxlogs.py "$@" meteor/infra-ui
