#!/bin/sh
set -eu
exec docker build --rm -t uws/heroku-logger -f docker/heroku/Dockerfile.logger ./docker/heroku
