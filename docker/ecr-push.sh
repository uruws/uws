#!/bin/sh
set -eu
IMG=${1:?'image name?'}

if test "${IMG}" = 'base'; then
	./docker/${IMG}/build.sh
else
	./${IMG}/build.sh
fi

docker rmi 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG} || true
docker tag uws/${IMG} 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG}
docker push 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG}

exit 0
