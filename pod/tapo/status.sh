#!/bin/sh
ns=${1:?'namespace?'}
app=${2:?'app name?'}
exec uwskube get all -n "${ns}" -l "app.kubernetes.io/name=meteor-${app}"
