#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}

# webapp-env

uwskube delete secret webapp-env -n "${uwscb_ns}" || true

uwskube create secret generic webapp-env -n "${uwscb_ns}" \
	--from-env-file=${HOME}/secret/chatbot/${UWSCB_ENV}/chatbot.env

exit 0
