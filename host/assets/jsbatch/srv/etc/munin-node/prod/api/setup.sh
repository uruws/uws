#!/bin/sh
set -eu

pl_ena=/root/bin/plugin-enable.sh

${pl_ena} http_loadtime http_loadtime

${pl_ena} contrib ssl/ssl-certificate-expiry ssl-certificate-expiry

exit 0
