#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/uwsbot ./docker/uwsbot
