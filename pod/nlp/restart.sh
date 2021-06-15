#!/bin/sh
set -eu
uwskube rollout -n ingress-nginx restart deploy/ner
uwskube rollout -n ingress-nginx restart deploy/sentiment
uwskube rollout -n ingress-nginx restart deploy/api
exit 0
