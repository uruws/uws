#!/bin/sh
set -eu
~/pod/tapo/cdn/restart.sh
~/pod/tapo/cdn/wait.sh
exec ~/pod/tapo/restart.sh "${TAPO_NAMESPACE}" web
