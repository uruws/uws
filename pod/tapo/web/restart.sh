#!/bin/sh
set -eu
~/pod/tapo/cdn/restart.sh
~/pod/tapo/cdn/wait.sh
echo '*** tapo-web'
exec ~/pod/tapo/restart.sh tapo web
