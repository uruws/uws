#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/eks ./docker/eks
