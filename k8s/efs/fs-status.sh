#!/bin/sh
set -eu
exec aws efs describe-file-systems \
	--output table \
	--region "${AWS_REGION}" \
	--query 'FileSystems[*].{FileSystemId: FileSystemId, Name: Tags[0].Value, SizeInBytes: SizeInBytes.Value, Status: LifeCycleState}'
