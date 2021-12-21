#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/nlpsvc/category/deploy.yaml
