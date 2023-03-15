#!/bin/sh
set -u
~/k8s/gateway/rollin.sh
exec ~/k8s/nginx/teardown.sh default
