#!/bin/sh
set -eu
exec ~/pod/lib/wait.sh worker Available deployment/meteor
