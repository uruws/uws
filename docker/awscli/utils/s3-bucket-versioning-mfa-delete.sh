#!/bin/sh
set -eu
token=${1:?'token?'}
exec aws s3api put-bucket-versioning \
	--region "${UWSBUCKET_REGION}" \
	--bucket "${AWS_CLOUDTRAIL_S3_BUCKET}" \
	--versioning-configuration Status=Enabled,MFADelete=Enabled \
	--mfa "${AWS_MFA_SERIAL} ${token}"
