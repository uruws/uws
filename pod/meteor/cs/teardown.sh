#!/bin/sh
set -eu
uwskube delete secret -n cs appenv || true
uwskube delete namespace cs
exit 0
