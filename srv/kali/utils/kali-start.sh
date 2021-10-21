#!/bin/sh
set -eu

x11vnc -display :0 -autoport -localhost -nopw -xkb -ncache -ncache_cr \
	-quiet -forever -create -bg &

sleep 3

exec /usr/share/novnc/utils/launch.sh --listen 8081 --vnc localhost:5900
