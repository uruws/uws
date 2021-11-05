#!/bin/sh
set -eu
~/pod/nlpsvc/configure.sh ${APP_ENV}
exec uwskube rollout -n nlpsvc restart deploy/nlpsvc
