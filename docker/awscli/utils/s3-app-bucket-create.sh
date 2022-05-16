#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}

# shellcheck disable=SC1090
. "${HOME}/config/s3/${bucket}.env"

exec aws s3api create-bucket \
	--bucket "${bucket}" \
	--acl private
