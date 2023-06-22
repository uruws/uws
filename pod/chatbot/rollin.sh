#!/bin/sh
set -eu
ns=cb${UWSCB_ENV}
exec uwskube delete -n "${ns}" -f ~/pod/chatbot/deploy.yaml
