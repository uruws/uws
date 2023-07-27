#!/bin/sh
set -eu
~/k8s/haproxy/setup.sh pod/tapo/srmnt
exec ~/pod/tapo/srmnt/hpx/install.sh
