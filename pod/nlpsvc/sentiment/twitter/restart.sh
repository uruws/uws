#!/bin/sh
set -eu
~/pod/nlpsvc/configure.sh "${NLPSVC_ENV}"
exec uwskube rollout -n nlpsvc restart deploy/sentiment-twitter
