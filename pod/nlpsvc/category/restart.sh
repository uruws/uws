#!/bin/sh
set -eu
exec uwskube rollout -n nlpsvc restart deploy/category
