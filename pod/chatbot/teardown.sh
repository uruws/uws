#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}
exec uwskube delete namespace "${uwscb_ns}"
