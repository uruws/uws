#!/bin/sh
set -eu
version=${1:-''}
~/pod/lib/deploy.sh nlp nlp/api ${version}
~/pod/lib/deploy.sh nlp nlp/ner
~/pod/lib/deploy.sh nlp nlp/sentiment
exit 0
