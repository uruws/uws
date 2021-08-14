#!/bin/sh
set -u
uwskube delete deploy munin-node -n mon
uwskube delete configmap cluster-setup -n mon
exit $?
