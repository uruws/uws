#!/bin/sh
set -eu
exec uwskube rollout -n nlpsvc restart deploy/sentiment-roberta
