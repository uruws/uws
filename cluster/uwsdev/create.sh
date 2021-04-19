#!/bin/sh
set -eu
name=${1:-'uwsdev'}
set -x
exec uwseks-cluster-create --profile uwsdev --region us-west-2 \
	--nodes 2 --nodes-min 2 --nodes-max 10 \
	--instance-types t3a.small \
	${name}
