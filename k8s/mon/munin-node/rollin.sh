#!/bin/sh
set -u
uwskube delete deploy munin-node -n mon
uwskube delete configmap node-setup    -n mon
uwskube delete configmap munin-plugins -n mon
uwskube delete configmap ops-ca        -n mon
uwskube delete configmap ops-ca-client -n mon
exit 0
