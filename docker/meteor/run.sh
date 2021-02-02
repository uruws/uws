#!/bin/sh
exec docker run -it --rm --name uws-meteor \
	--hostname meteor.uws.local -u root uws/meteor
