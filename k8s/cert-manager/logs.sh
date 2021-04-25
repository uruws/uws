#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube -n cert-manager logs deployment.apps/cert-manager $@
