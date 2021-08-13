#!/bin/sh
set -u
uwskube delete secret cluster-env -n mon
exec uwskube delete namespace mon
