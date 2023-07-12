#!/bin/sh
set -eu
PYTHONPATH=/opt/uws/lib:/opt/uws/lib/test
export PYTHONPATH
exec /opt/uws/venv/bin/python3 -m mypy /opt/uws/lib
