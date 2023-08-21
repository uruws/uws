#!/bin/sh
set -eu
exec ~/pod/tapo/ngxlogs.py tapo/cdn "$@"
