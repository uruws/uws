#!/bin/sh
set -u
uwskube delete secret cluster-auth -n mon
uwskube delete configmap cluster-env -n mon
exec uwskube delete namespace mon
