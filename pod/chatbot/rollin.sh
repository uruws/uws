#!/bin/sh
set -eu
exec uwskube delete -f ~/pod/chatbot/deploy.yaml
