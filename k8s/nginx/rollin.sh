#!/bin/sh
set -eu
exec uwskube delete deploy proxy -n nginx
