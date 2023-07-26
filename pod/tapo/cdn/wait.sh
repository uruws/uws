#!/bin/sh
set -eu
exec ~/pod/tapo/wait.sh "${TAPO_NAMESPACE}" cdn
