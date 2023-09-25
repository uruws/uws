#!/bin/sh
set -eu
exec docker run -it --rm --name uws-munin-node \
	--hostname munin-node.uws.local \
	-u root uws/munin-node-2309
