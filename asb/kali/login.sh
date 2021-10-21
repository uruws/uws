#!/bin/sh
set -eu
exec ssh -i secret/asb/ssh/kali -l kali \
	${1:?'hostname?'}.uws.talkingpts.org
