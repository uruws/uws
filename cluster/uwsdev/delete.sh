#!/bin/sh
set -eu
name=${1:-'uwsdev'}

set -x

uwseks-cluster-delete --profile uwsdev --region us-west-2 ${name}

exit 0
