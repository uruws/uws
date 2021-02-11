#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/base-testing ./docker/base-testing
