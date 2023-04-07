#!/bin/sh
set -eu
exec uwskube get all,pvc -n grfn
