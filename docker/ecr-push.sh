#!/bin/sh
set -eu

IMG=${1:?'image name?'}

if test -x ./docker/${IMG}/build.sh; then
	./docker/${IMG}/build.sh
elif test -x ./${IMG}/build.sh; then
	./${IMG}/build.sh
else
	echo "invalid image name: '${IMG}'" >&2
	exit 1
fi

ENV=${ENV:-'dev'}

REGURI="789470191893.dkr.ecr.us-east-1.amazonaws.com/uws"
if test "${ENV}" != 'prod'; then
	REGURI="${REGURI}${ENV}"
fi

docker rmi ${REGURI}:${IMG} || true

docker tag uws/${IMG} ${REGURI}:${IMG}
docker push ${REGURI}:${IMG}

exit 0
