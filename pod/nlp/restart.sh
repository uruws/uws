#!/bin/sh
set -eu
uwskube rollout -n nlp restart deploy/ner
uwskube rollout -n nlp restart deploy/sentiment
uwskube rollout -n nlp restart deploy/api
exit 0
