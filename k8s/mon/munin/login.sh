#!/bin/sh
set -eu
container=${1:-munin}
exec uwskube exec pod/munin-0 -i -t -c "${container}" -n mon -- bash -il
