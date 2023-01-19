#!/bin/sh
set -eu
servername='ops.uws.talkingpts.org'
ssh_cmd="ssh -a -n -x"
exec ${ssh_cmd} -l uws "${servername}" docker logs herokud "$@"
