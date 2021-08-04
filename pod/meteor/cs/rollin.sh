#!/bin/sh
set -eu
uwskube delete hpa meteor-hpa -n cs || true
uwskube delete deploy meteor -n cs
exit 0
