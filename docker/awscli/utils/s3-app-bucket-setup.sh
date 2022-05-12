#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}
. "${HOME}/config/s3/${bucket}.env"

~/bin/s3-app-bucket-policy.sh "${bucket}"
~/bin/s3-app-bucket-cors.sh "${bucket}"

exit 0
