#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/nlpsvc/sentiment/twitter/deploy.yaml
