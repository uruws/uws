#!/bin/sh
set -eu
uwskube delete deploy kubeshark -n mon
exec ~/k8s/mon/kubeshark/clean.sh
