#!/bin/sh
set -u
~/k8s/gateway/ngx/rollin.sh
exec ~/k8s/nginx/teardown.sh default
