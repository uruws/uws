#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}
. "${HOME}/config/s3/${bucket}.env"

~/bin/s3-app-bucket-policy.sh "${bucket}"
~/bin/s3-app-bucket-cors.sh "${bucket}"

aws s3api put-bucket-versioning \
	--bucket "${bucket}" \
	--versioning-configuration Status=Enabled

exit 0
