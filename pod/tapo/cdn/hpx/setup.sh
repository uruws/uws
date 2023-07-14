#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh pod/tapo/cdn/hpx
exec ~/pod/tapo/cdn/hpx/install.sh
