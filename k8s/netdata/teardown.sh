#!/bin/sh
set -eu
helm uninstall --namespace netdata netdata
exec uwskube delete namespace netdata
