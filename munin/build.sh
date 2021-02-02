#!/bin/sh
set -eu
exec docker build $@ --rm -t uws/munin ./munin
