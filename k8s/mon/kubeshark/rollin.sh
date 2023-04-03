#!/bin/sh
set -u
uwskube delete deploy kubeshark -n mon
~/k8s/mon/kubeshark/gw/rollin.sh
exec ~/k8s/mon/kubeshark/clean.sh
