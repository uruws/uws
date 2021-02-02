#!/bin/sh
set -eu
exec docker build --rm -t uws/meteor ./docker/meteor
