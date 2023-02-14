#!/bin/sh
set -eu
exec helm uninstall aws-efs-csi-driver
