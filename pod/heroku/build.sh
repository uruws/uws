#!/bin/sh
set -eu
exec docker build --rm -t uwspod/heroku ./pod/heroku
