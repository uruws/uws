#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh pod/tapo/api/hpx
exec ~/pod/tapo/api/hpx/install.sh
