#!/bin/sh
set -eu
appenv=${1:?'app env?'}
envf=${HOME}/secret/nlpsvc/${appenv}.env
uwskube delete secret -n nlpsvc nlpsvc-env || true
uwskube create secret generic -n nlpsvc nlpsvc-env --from-env-file="${envf}"
exit 0
