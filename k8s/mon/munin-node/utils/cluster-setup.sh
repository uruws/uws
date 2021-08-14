#!/bin/sh
set -eu

enpl=/root/bin/plugin-enable.sh

${enpl} local k8smon nodes

exit 0
