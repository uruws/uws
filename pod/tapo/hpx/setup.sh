#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh pod/tapo/hpx
exec ~/pod/tapo/hpx/install.sh
