#!/bin/sh
set -eu
mkdir -vp ./pod/test/build

./docker/golang/cmd.sh build -o /go/build/cmd/podtest.bin ./cmd/podtest
mv -vf ./docker/golang/build/podtest.bin ./pod/test/build/podtest

docker build --rm -t uws/pod:test ./pod/test

rm -rf ./pod/test/build
exit 0
