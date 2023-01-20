#!/bin/sh
set -eu
webapp=${UWS_WEBAPP}
PYTHONPATH=/opt/uws/${webapp}
export PYTHONPATH
exec /opt/uws/venv/bin/python3 -m mypy "/opt/uws/${webapp}"