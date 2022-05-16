#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}

# shellcheck disable=SC1090
. "${HOME}/config/s3/${bucket}.env"

~/bin/s3-app-bucket-policy.sh "${bucket}"
~/bin/s3-app-bucket-cors.sh "${bucket}"
~/bin/s3-app-bucket-versioning.sh "${bucket}"
~/bin/s3-app-bucket-encryption.sh "${bucket}"

exit 0
