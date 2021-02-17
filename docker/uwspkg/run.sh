#!/bin/sh
exec docker run -it --rm --network none --name uws-uwspkg \
	--hostname uwspkg.uws.local \
	-u uws uws/uwspkg $@
