#!/bin/sh
set -eu
uwskube delete service meteor -n web
uwskube delete namespace web
exit 0
