#!/bin/sh
set -eu
IMG=${1:?'image name?'}

./docker/${IMG}/build.sh

docker rmi 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG}
docker tag uws/${IMG} 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG}
docker push 789470191893.dkr.ecr.us-east-1.amazonaws.com/uws:${IMG}

exit 0
