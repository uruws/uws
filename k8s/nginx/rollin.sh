#!/bin/sh
set -eu
uwskube delete service proxy -n nginx
exec uwskube delete deploy proxy -n nginx
