#!/bin/sh
set -eu
exec ~/pod/tapo/restart.sh "${TAPO_CDN_NAMESPACE}" cdn
