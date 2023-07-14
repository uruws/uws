#!/bin/sh
set -eu
~/pod/tapo/cdn/status.sh
exec ~/pod/tapo/status.sh tapo web
