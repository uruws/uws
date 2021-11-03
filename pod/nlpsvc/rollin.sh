#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/nlpsvc/deploy.yaml
