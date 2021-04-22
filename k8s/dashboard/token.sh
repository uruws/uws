#!/bin/sh
set -eu
. ~/bin/env.export
exec uwskube -n kube-system describe secret $(uwskube -n kube-system get secret | grep uwsadm-token | awk '{print $1}')
