#!/bin/sh
set -eu
uwscb_ns="cb${UWSCB_ENV}"
exec uwskube create namespace "${uwscb_ns}"
