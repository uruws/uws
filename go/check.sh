#!/bin/sh
set -eu
cd /go/src/uws
exec run-parts --verbose --regex='\.sh$' --exit-on-error ./testing/run
