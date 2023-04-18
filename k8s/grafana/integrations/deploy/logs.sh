#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n grfn deployment.apps/grafana-agent-integrations-deploy
