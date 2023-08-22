#!/bin/sh
set -eu
exec ~/pod/tapo/wait.sh "${TAPO_CDN_NAMESPACE}" cdn
