#!/bin/sh
set -eu
exec uwskube logs --tail=10 --timestamps -n ingress-nginx service/ingress-nginx-controller $@
