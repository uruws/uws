#!/bin/sh
set -eu
exec aws iam create-policy \
	--policy-name UserMFA \
	--policy-document "file://${HOME}/config/iam/UserMFA.json"
