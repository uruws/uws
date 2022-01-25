#!/bin/sh
set -eu
exec python3 -m mypy ${HOME}/test/plugins /uws/lib/plugins
