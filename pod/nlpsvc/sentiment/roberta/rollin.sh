#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/nlpsvc/sentiment/roberta/deploy.yaml
