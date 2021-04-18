#!/bin/sh
set -eu
name=${1:-'uwsdev'}

set -x

uwseks-cluster-create --profile uwsdev --region us-west-2 \
	--nodes 2 --nodes-min 2 --nodes-max 10 \
	--instance-types t3a.small \
	${name}

uwseks-cluster-setup-dashboard ${name}
uwseks-cluster-setup-metrics-server ${name}

exit 0
