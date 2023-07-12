#!/bin/sh
set -eu
exec docker run -it --rm --name uws-munin-node-devel \
	--hostname munin-node-devel.uws.local \
	-u root --entrypoint /bin/bash uws/munin-node-2305
