#!/bin/sh
set -eu
appenv=${1:?'app env?'}
envf=${HOME}/secret/eks/files/nlpsvc/${appenv}.env

uwskube delete secret -n nlpsvc nlpsvc-env || true
uwskube create secret generic -n nlpsvc nlpsvc-env --from-env-file="${envf}"

uwskube delete secret -n nlpsvc etcdir || true
uwskube create secret generic -n nlpsvc etcdir \
	--from-file=${HOME}/secret/eks/files/nlpsvc/etc/

exit 0
