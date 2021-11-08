#!/bin/sh
set -eu
exec jupyter notebook --ip=127.0.0.1 --port=8888 --port-retries=1 \
	--no-browser --autoreload --notebook-dir=/srv/home/jupyter
