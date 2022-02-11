#!/bin/sh
set -eu
exec /srv/deploy/Buildpack/build.py "$@"
