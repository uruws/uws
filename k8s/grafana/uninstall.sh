#!/bin/sh
set -eu
exec helm uninstall --namespace grfn grafana
