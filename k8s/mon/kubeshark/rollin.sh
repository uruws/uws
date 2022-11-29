#!/bin/sh
set -u
uwskube delete ingress kubeshark-gateway
uwskube delete service kubeshark -n mon
exec uwskube delete deploy kubeshark -n mon
