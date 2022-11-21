#!/bin/sh
set -eu
exec ~/bin/uwseks scale nodegroup -n main -C false "$@"
