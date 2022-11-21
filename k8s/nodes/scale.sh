#!/bin/sh
set -eu
exec uwseks scale nodegroup -n main -C false "$@"
