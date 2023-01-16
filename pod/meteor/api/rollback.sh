#!/bin/sh
set -eu
exec ~/pod/lib/rollback.sh api deployment/meteor
