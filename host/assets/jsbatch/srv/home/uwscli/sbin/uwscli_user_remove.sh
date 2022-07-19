#!/bin/sh
set -u
umask 0027
username=${1:?'username?'}
userdel -f -r "${username}"
groupdel -f "${username}"
exit 0
