#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}

# shellcheck disable=SC1090
. "${HOME}/config/s3/${bucket}.env"

exec aws s3api put-bucket-cors \
	--region "${UWSBUCKET_REGION}" \
	--bucket "${bucket}" \
	--cors-configuration "file://${HOME}/config/s3/${UWSBUCKET_CORS}"
