#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}
exec uwskube exec deployment/webapp -n "${uwscb_ns}" -it -- /bin/bash -il
