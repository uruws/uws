#!/bin/sh
set -eu

appver=${1:?'app version?'}

set -x

~/pod/tapo/worker/deploy.sh "${appver}"
~/pod/tapo/api/deploy.sh    "${appver}"
~/pod/tapo/web/deploy.sh    "${appver}"

~/pod/tapo/worker/wait.sh
~/pod/tapo/api/wait.sh
~/pod/tapo/web/wait.sh

exit 0
