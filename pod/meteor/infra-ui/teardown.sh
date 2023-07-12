#!/bin/sh
set -u
ns="infra-ui-${INFRA_UI_ENV}"
uwskube delete secret -n "${ns}" appenv || true
uwskube delete service meteor -n "${ns}"
uwskube delete namespace "${ns}"
exit 0
