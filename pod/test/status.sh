#!/bin/sh
exec ~/pod/lib/status.sh default all \
	-l 'app.kubernetes.io/name=podtest'
