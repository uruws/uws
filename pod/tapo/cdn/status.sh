#!/bin/sh
set -eu
exec ~/pod/tapo/status.sh "${TAPO_CDN_NAMESPACE}" cdn
