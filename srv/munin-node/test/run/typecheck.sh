#!/bin/sh
set -eu
exec python3 -m mypy ${HOME}/test /uws/lib/plugins
