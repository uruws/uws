#!/bin/sh
set -eu
exec docker build --rm -t uws/pod:base ./pod/base
