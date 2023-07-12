#!/bin/sh
set -eu
webapp=${UWS_WEBAPP}
PYTHONPATH=/opt/uws/lib:/opt/uws/${webapp}:/etc/opt/uws/${webapp}:/opt/uws/${webapp}/test
export PYTHONPATH
exec /opt/uws/venv/bin/python3 -m mypy /opt/uws/lib "/opt/uws/${webapp}" "/etc/opt/uws/${webapp}"
