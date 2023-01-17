#!/bin/sh
set -eu
exec ~/pod/lib/wait.sh web deployment/meteor
