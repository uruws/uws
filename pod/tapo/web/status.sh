#!/bin/sh
set -eu
~/pod/tapo/cdn/status.sh
echo '*** tapo-web'
exec ~/pod/tapo/status.sh tapo web
