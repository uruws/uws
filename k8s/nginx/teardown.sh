#!/bin/sh
set -eu
uwskube delete service proxy -n nginx
sleep 1
exec uwskube delete namespace nginx
