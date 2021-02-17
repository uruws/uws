#!/bin/sh
set -eu

IMG=${1:?'image name?'}

if test -x ./docker/${IMG}/build.sh; then
	./docker/${IMG}/build.sh
elif test -x ./srv/${IMG}/build.sh; then
	./srv/${IMG}/build.sh
else
	echo "invalid image name: '${IMG}'" >&2
	exit 1
fi

ENV=${ENV:-'dev'}

AWS_REGION=${AWS_REGION:-'us-east-1'}
REGURI="789470191893.dkr.ecr.${AWS_REGION}.amazonaws.com/uws"
if test "${ENV}" != 'prod'; then
	REGURI="${REGURI}${ENV}"
fi

echo "i - ecr push: ${REGURI}"

docker rmi ${REGURI}:${IMG} || true

docker tag uws/${IMG} ${REGURI}:${IMG}
docker push ${REGURI}:${IMG}

exit 0
