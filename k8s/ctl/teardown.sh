#!/bin/sh
set -u
~/k8s/ctl/rollin.sh
exec uwskube delete namespace ctl
