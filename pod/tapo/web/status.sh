#!/bin/sh
set -eu
~/pod/tapo/cdn/status.sh
echo
exec ~/pod/tapo/status.sh "${TAPO_NAMESPACE}" web
