#!/bin/sh
set -eu
export SSH_KEYNAME=kali
exec ~/asb/run.sh $@ ./kali/deploy.yaml
