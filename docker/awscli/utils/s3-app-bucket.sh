#!/bin/sh
set -u

bucket=${1:?'bucket name?'}

echo '*** acl'
aws s3api get-bucket-acl --bucket "${bucket}"

echo '*** cors'
aws s3api get-bucket-cors --bucket "${bucket}"

echo '*** lifecycle-configuration'
aws s3api get-bucket-lifecycle-configuration --bucket "${bucket}"

echo '*** policy'
aws s3api get-bucket-policy --bucket "${bucket}"

echo '*** versioning'
aws s3api get-bucket-versioning --bucket "${bucket}"

exit 0
