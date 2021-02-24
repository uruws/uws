#!/bin/sh
set -eu
mkdir -vp ./docker/golang/tmp
cp -va ./go/go.mod ./go/go.sum ./docker/golang/tmp/
exec docker build $@ --rm -t uws/golang ./docker/golang
