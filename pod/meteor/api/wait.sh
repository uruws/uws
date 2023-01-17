#!/bin/sh
set -eu
exec ~/pod/lib/wait.sh api deployment/meteor
