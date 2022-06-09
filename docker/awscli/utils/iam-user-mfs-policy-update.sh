#!/bin/sh
set -eu
exec aws iam create-policy-version \
	--set-as-default \
	--policy-arn ${AWS_USER_MFA_POLICY_ARN} \
	--policy-document "file://${HOME}/config/iam/${AWS_USER_MFA_POLICY_DOC}"
