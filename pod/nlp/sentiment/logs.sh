#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n nlp -l 'app.kubernetes.io/name=nlp-sentiment' --max 20 $@
