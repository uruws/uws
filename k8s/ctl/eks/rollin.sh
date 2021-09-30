#!/bin/sh
set -u
exec uwskube delete cronjob eks-nodegroup-upgrade -n ctl
