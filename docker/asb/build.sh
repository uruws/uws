#!/bin/sh
set -eu
docker build $@ --rm -t uws/ansible ./docker/asb
exit 0
