#!/bin/sh
set -eu
ns=cs
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=tapo
export METEOR_HOST=${METEOR_CS_HOST}
exec ~/pod/meteor/gw/rollin.sh "${ns}"
