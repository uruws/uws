#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/nlpsvc/topic/automl/deploy.yaml
