#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}
. "${HOME}/config/s3/${bucket}.env"

exec aws s3api put-bucket-policy \
	--bucket "${bucket}" \
	--policy "file://${HOME}/config/s3/${UWSBUCKET_POLICY}"
