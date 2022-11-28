#!/bin/sh
set -u
uwskube delete ingress kubeshark-gateway
exec uwskube delete deploy kubeshark -n mon
