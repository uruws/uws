#!/bin/sh
set -eu

appenv=${1:?'app.env?'}

uwskube delete secret -n meteor-worker meteor-worker-env || true
uwskube create secret generic -n meteor-worker meteor-worker-env \
	--from-file="app.env=${appenv}"

crtfn=${HOME}/ca/cert/nlp/meteor-worker.crt
keyfn=${HOME}/ca/cert/nlp/meteor-worker.key

uwskube delete secret -n meteor-worker nlp-client-cert || true
uwskube create secret generic -n meteor-worker nlp-client-cert \
	--from-file="tls.crt=${crtfn}" --from-file="tls.key=${keyfn}"

exit 0
