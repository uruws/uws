#!/bin/sh
set -eu
export WEBAPP_PORT=2741
exec ./docker/webapp/devel.sh chatbot
