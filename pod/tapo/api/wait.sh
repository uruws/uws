#!/bin/sh
set -eu
exec ~/pod/tapo/wait.sh "${TAPO_API_NAMESPACE}" api
