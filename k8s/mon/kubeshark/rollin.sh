#!/bin/sh
set -u
uwskube delete deploy  kubeshark -n mon
uwskube delete service kubeshark -n mon
~/k8s/mon/kubeshark/clean.sh
exit 0
