#!/bin/sh
set -eu
hostname=${1:?'hostname?'}
username=${2:?'username?'}
shift
shift
exec /usr/bin/ssh -q -a -C -n -x \
	-F /etc/opt/uws/chatbot/ssh/config \
	-i /etc/opt/uws/chatbot/ssh/ecdsa_id \
	-l "${username}" "${hostname}" "$@"
