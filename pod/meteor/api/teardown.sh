#!/bin/sh
set -eu
uwskube delete service   meteor -n api
uwskube delete namespace api
exit 0
