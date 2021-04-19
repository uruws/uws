#!/bin/sh
set -eu
name=${1:-'uwsdev'}

set -x

uwseks-cluster-teardown-cert-manager ${name}
uwseks-cluster-teardown-metrics-server ${name}
uwseks-cluster-teardown-dashboard ${name}

uwseks-cluster-delete --profile uwsdev --region us-west-2 --wait ${name}

exit 0
