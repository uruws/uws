#!/bin/sh
set -eu
exec uwskube delete deploy meteor -n worker
