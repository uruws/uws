#!/bin/sh
set -eu
namespace=${1:?'namespace?'}
exec uwskube top pods -n "${namespace}"
