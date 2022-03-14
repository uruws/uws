#!/bin/sh
set -eu
uwskube delete secret -n infra-ui appenv || true
exec uwskube delete namespace infra-ui
