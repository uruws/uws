#!/bin/sh
set -eu
mkdir -vp ./docker/golang/tmp
install -C -v -m 640 ./go/go.mod ./go/go.sum ./docker/golang/tmp/
exec docker build $@ --rm -t uws/golang ./docker/golang
