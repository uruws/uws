#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}

# shellcheck disable=SC1090
. "${HOME}/config/s3/${bucket}.env"

set +e

echo '*** acl'
aws s3api get-bucket-acl --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

echo '*** cors'
aws s3api get-bucket-cors --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

echo '*** lifecycle-configuration'
aws s3api get-bucket-lifecycle-configuration --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

echo '*** policy'
aws s3api get-bucket-policy --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

echo '*** versioning'
aws s3api get-bucket-versioning --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

echo '*** encryption'
aws s3api get-bucket-encryption --region "${UWSBUCKET_REGION}" \
	--output json --bucket "${bucket}"

exit 0
