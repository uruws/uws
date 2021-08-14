#!/bin/sh
set -u
uwskube delete deploy munin-node -n mon
uwskube delete configmap cluster-setup -n mon
uwskube delete svc munin-node -n mon
exit $?
