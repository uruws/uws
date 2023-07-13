#!/bin/sh
set -eu
~/pod/tapo/cdn/rollin.sh
exec ~/pod/tapo/rollin.sh tapo web
