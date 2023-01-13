#!/bin/sh
set -eu
region=${1:?'region?'}
exec aws logs describe-log-groups --region "${region}"
