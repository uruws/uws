#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/k8s ./docker/k8s
