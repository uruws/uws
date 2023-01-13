#!/bin/sh
set -eu
exec ~/pod/lib/wait.sh api Available deployment/meteor
