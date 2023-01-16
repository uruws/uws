#!/bin/sh
set -eu
exec ~/pod/lib/rollback.sh worker meteor/worker
