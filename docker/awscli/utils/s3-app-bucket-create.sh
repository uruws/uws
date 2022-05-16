#!/bin/sh
set -eu

bucket=${1:?'bucket name?'}
. "${HOME}/config/s3/${bucket}.env"

exec aws s3api create-bucket \
	--bucket "${bucket}" \
	--acl public-read
