#!/bin/sh
set -eu
exec aws elbv2 describe-load-balancers --region "${AWS_REGION}" --output text
