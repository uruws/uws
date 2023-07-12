#!/bin/sh
set -eu

~/bin/ecr-login.sh sa-east-1

docker pull 789470191893.dkr.ecr.sa-east-1.amazonaws.com/uwsops:acme
docker tag  789470191893.dkr.ecr.sa-east-1.amazonaws.com/uwsops:acme uwsops:acme

exec docker system prune -f
