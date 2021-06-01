#!/bin/sh
set -eu
uwskube delete configmap promcfg -n mon
uwskube delete namespace mon
exit 0
