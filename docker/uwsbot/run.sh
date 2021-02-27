#!/bin/sh
exec docker run --rm --network none --name uws-uwsbot \
	--hostname uwsbot.uws.local -u uws uws/uwsbot $@
