#!/bin/sh
set -eu
if ! test -d ~/.local/share/jupyter/kernels/python3; then
	ipython3 kernel install --user
fi
exec jupyter-notebook --ip=127.0.0.1 --port=8888 --port-retries=1 \
	--no-browser --autoreload --notebook-dir=/srv/home \
	--NotebookApp.trust_xheaders=True \
	--NotebookApp.allow_remote_access=True
