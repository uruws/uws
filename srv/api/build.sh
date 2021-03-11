#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/api ./srv/api
