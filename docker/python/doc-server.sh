#!/bin/sh
set -eu
exec ./docker/python/doc.sh -p 6080 -n 0.0.0.0
