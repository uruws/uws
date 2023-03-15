#!/bin/sh
set -u
exec uwskube delete service k8s -n mon
