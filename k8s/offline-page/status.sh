#!/bin/sh
set -eu
exec uwskube get all | grep -E '^NAME|offline-page|^$'
