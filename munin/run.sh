#!/bin/sh
exec docker run -it --rm --name uws-munin \
	--hostname munin.uws.local -u root uws/munin
