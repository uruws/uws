#!/bin/sh
set -eu
exec uwseks-cluster-create --profile amybeta --region us-east-2 \
	--nodes 5 --nodes-min 3 --nodes-max 50 \
	--instance-types t3a.large,t3a.medium,t3a.small \
	amybeta
