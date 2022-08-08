#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube delete service "offline-page-${ns}"
