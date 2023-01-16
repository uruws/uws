#!/bin/sh
set -eu
exec ~/pod/lib/rollback.sh web deployment/meteor
