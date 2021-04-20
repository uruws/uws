#!/bin/sh
set -eu

region=${1:?'region?'}
src_img=${2:?'source image name?'}
dst_img=${3:?'dest image name?'}

dst_uri="789470191893.dkr.ecr.${region}.amazonaws.com/${dst_img}"
echo "i - ecr push: ${src_img} -> ${dst_uri}"

docker tag ${src_img} ${dst_uri}
docker push ${dst_uri}

exit 0
