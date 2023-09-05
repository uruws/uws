#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
exec ~/pod/lib/wait.sh "${ns}" "deployment/meteor-${app}"
