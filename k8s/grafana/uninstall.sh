#!/bin/sh
set -u
~/k8s/grafana/rollin.sh
exec helm uninstall --namespace grfn grafana
