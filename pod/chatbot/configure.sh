#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}

# webapp-env

uwskube delete secret webapp-env -n "${uwscb_ns}" || true

uwskube create secret generic webapp-env -n "${uwscb_ns}" \
	--from-env-file=${HOME}/secret/chatbot/${UWSCB_ENV}/chatbot.env

# webapp-conf

uwskube delete secret webapp-conf -n "${uwscb_ns}" || true

uwskube create secret generic webapp-conf -n "${uwscb_ns}" \
	--from-file=${HOME}/secret/chatbot/${UWSCB_ENV}/config

# webapp-conf-ssh

uwskube delete secret webapp-conf-ssh -n "${uwscb_ns}" || true

uwskube create secret generic webapp-conf-ssh -n "${uwscb_ns}" \
	--from-file=${HOME}/secret/chatbot/${UWSCB_ENV}/config/ssh

exit 0
