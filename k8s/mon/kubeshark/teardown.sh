#!/bin/sh
set -u
uwskube delete service kubeshark -n mon
uwskube delete ingress kubeshark-gateway
uwskube delete service kubeshark
exit 0
