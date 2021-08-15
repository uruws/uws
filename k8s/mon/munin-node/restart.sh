#!/bin/sh
set -eu
exec uwskube rollout restart deploy munin-node -n mon
