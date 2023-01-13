#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws sns create-topic \
	--region "${region}" \
	--name GuardDutyEmail
