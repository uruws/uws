#!/bin/sh
set -eu
pl_ena=/root/bin/plugin-enable.sh
${pl_ena} http_loadtime http_loadtime
exit 0
