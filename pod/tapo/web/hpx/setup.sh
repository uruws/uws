#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh pod/tapo/web/hpx
exec ~/pod/tapo/web/hpx/install.sh
