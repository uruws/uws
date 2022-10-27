#!/bin/sh
set -eu
(ssh -a -n -x -l uws janis.uws.talkingpts.org sudo -n rm -rvf /uws/init) || true
./host/deploy.sh janis.uws.talkingpts.org janis
ssh -a -n -x -l uws janis.uws.talkingpts.org tail -f /var/log/cloud-init-output.log
exit 0
