#!/bin/sh
set -u
uwskube delete deploy kubeshark -n mon
exec ~/k8s/mon/kubeshark/clean.sh
