#!/bin/sh
set -eu
pod=$(uwskube get pod -n mon -o name -l app.kubernetes.io/name=grafana)
exec uwskube exec -it ${pod} -c grafana -- /bin/sh
