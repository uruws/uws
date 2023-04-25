#!/bin/sh
set -eu
exec uwskube delete -n default -f ~/pod/test/deploy.yaml
