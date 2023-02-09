#!/bin/sh
set -u
uwskube delete service proxy         -n nginx
uwskube delete deploy  proxy         -n nginx
uwskube delete secret  proxy-env     -n nginx
uwskube delete secret  sites-enabled -n nginx
uwskube delete secret  tapo-tls      -n nginx
exit 0
