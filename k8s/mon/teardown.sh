#!/bin/bash
set -u
~/k8s/mon/rollin.sh
~/k8s/mon/munin/teardown.sh
~/k8s/mon/munin-node/teardown.sh
exec uwskube delete namespace mon
