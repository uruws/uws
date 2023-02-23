#!/bin/sh
set -u
uwskube scale sts munin --replicas=0 -n mon
uwskube delete configmap munin-confd -n mon --wait
uwskube delete sts munin -n mon
exit 0
