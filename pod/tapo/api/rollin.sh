#!/bin/sh
set -eu
exec ~/pod/tapo/rollin.sh "${TAPO_API_NAMESPACE}" api
