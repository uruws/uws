#!/bin/sh
set -eu
passwd=$(uwskube get secret -n mon tobs-grafana -o jsonpath='{.data.admin-password}' | base64 -d)
echo "https://${UWS_CLUSTER}.uws.talkingpts.org/"
echo "admin -> ${passwd}"
exit 0
