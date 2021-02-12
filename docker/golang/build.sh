#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/golang ./docker/golang
