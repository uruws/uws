#!/bin/sh
set -eu
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	-u root --entrypoint /bin/bash uws/munin
