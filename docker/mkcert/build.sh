#!/bin/sh
set -eu
exec docker build --rm -t uws/mkcert ./docker/mkcert
