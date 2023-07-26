#!/bin/sh
set -eu
exec ~/pod/tapo/restart.sh "${TAPO_NAMESPACE}" cdn
