#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}

# shellcheck disable=SC1090
. "${HOME}/config/s3/${bucket}.env"

exec aws s3api put-bucket-versioning \
	--bucket "${bucket}" \
	--versioning-configuration Status=Enabled
