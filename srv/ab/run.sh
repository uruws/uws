#!/bin/sh
set -eu
exec ./docker/webapp/devel.sh ab --exec
