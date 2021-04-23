#!/bin/sh
set -eu
eksenv=${1:?'cluster env?'}
. ./eks/env/${eksenv}.env
exec ./docker/eks/admin.sh --client
