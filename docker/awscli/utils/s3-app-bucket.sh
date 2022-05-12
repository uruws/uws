#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}
. "${HOME}/config/s3/${bucket}.env"

set +e

echo '*** acl'
aws s3api get-bucket-acl --output json --bucket "${bucket}"

echo '*** cors'
aws s3api get-bucket-cors --output json --bucket "${bucket}"

echo '*** lifecycle-configuration'
aws s3api get-bucket-lifecycle-configuration --output json --bucket "${bucket}"

echo '*** policy'
aws s3api get-bucket-policy --output json --bucket "${bucket}"

echo '*** versioning'
aws s3api get-bucket-versioning --output json --bucket "${bucket}"

exit 0
