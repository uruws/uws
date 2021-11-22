#!/bin/sh
set -eu
ipython3 kernel install --user
exec jupyter notebook --ip=127.0.0.1 --port=8888 --port-retries=1 \
	--no-browser --autoreload --notebook-dir=/srv/home/jupyter \
	--NotebookApp.allow_remote_access=True
