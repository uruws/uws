#!/bin/sh
set -eu
uwscb_ns="cb${UWSCB_ENV}"
exec uwskube delete -n "${uwscb_ns}" -f ~/pod/chatbot/deploy.yaml
