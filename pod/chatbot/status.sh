#!/bin/sh
uwscb_ns=cb${UWSCB_ENV}
exec ~/pod/lib/status.sh "${uwscb_ns}" all
