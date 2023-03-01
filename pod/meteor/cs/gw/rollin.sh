#!/bin/sh
set -eu
ns=cs
export METEOR_NAMESPACE=${ns}
export METEOR_HOST=${METEOR_CS_HOST}
export METEOR_TLS=tapo
exec ~/pod/meteor/gw/rollin.sh "${ns}"
