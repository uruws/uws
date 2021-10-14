#!/bin/sh
set -eu
exec ssh -i secret/asb/ssh/rstudio -l admin \
	${1:?'hostname?'}.uws.talkingpts.org
