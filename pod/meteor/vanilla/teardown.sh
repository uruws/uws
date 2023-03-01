#!/bin/sh
set -u
uwskube delete secret -n meteor-vanilla appenv || true
uwskube delete service meteor -n meteor-vanilla
exec uwskube delete namespace meteor-vanilla
