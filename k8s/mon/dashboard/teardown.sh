#!/bin/sh
set -u
uwskube delete ingress mon-dashboard
exec uwskube delete service grafana
