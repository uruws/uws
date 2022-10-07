#!/bin/sh
set -eu
clienv="${UWSCLI_ENV}"
echo "${clienv}.cli.uws.talkingpts.org" >/etc/mailname
exit 0
