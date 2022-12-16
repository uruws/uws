#!/bin/sh
set -u
uwskube delete ingress kubeshark-gateway
exec uwskube delete service kubeshark -n mon
