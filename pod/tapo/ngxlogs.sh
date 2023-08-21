#!/bin/sh
set -eu
pod="${1:?'ngx pod?'}"
shift
exec ~/pod/lib/ngxlogs.py --name ngx "$@" "${pod}"
