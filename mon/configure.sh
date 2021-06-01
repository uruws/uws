#!/bin/sh
set -eu
uwskube create configmap promcfg -n mon --from-file=${HOME}/mon/etc/prometheus/
exit 0
