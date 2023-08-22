#!/bin/sh
set -eu
exec ~/pod/tapo/rollin.sh "${TAPO_CDN_NAMESPACE}" cdn
