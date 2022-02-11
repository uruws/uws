#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/test/deploy.yaml
