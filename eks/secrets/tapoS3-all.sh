#!/bin/sh
set -eu
./eks/secrets/tapoS3-update.py Test ./secret/eks/files/meteor/app/staging-settings.json
./eks/secrets/tapoS3-update.py Live ./secret/eks/files/meteor/app/prod-settings.json
exit 0
