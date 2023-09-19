#!/bin/sh
set -eu
exec uwskube get all,ingress -A
