#!/bin/sh
set -eu
exec docker build --rm -t uwspod/base ./pod/base
