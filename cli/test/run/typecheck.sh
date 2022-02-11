#!/bin/sh
set -eu
export PYTHONPATH=/srv/home/uwscli/lib:/srv/uws/deploy/cli:${HOME}/test
exec python3 -m mypy --exclude local_conf.py \
	/srv/uws/deploy/cli /srv/home/uwscli/lib
