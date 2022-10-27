#!/bin/sh
set -eu
./host/deploy.sh janis.uws.talkingpts.org janis
ssh -a -n -x -l uws janis.uws.talkingpts.org tail -f /var/log/cloud-init-output.log
exit 0
