#!/bin/sh
set -eu
profile="${UWSCLI_PROFILE}"
echo "${profile}.cli.uws.talkingpts.org" >/etc/mailname
exit 0
