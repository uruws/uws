#!/bin/sh
set -eu
exec aws iam create-policy \
	--policy-name ${AWS_USER_MFA_POLICY} \
	--policy-document "file://${HOME}/config/iam/${AWS_USER_MFA_POLICY_DOC}"
