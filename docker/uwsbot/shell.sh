#!/bin/sh
set -eu
exec docker run -it --rm --name uws-bot-shell \
	--hostname bot-shell.uws.local \
	-e "UWS_LOG=quiet" \
	-e "UWS_PREFIX=/uws" \
	--entrypoint /bin/bash \
	-u root uws/uwsbot-2305
