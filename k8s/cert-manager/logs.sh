#!/bin/sh
set -eu
exec uwskube -n cert-manager logs -l 'app.kubernetes.io/instance=cert-manager' "$@"
