#!/bin/sh
set -eu
exec uwskube get all,cm,secret -n nginx
