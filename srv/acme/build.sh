#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/acme ./srv/acme
