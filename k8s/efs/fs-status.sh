#!/bin/sh
set -eu
exec aws efs describe-file-systems \
	--output table \
	--region "${AWS_REGION}" \
	--query 'FileSystems[*].{FileSystemId: FileSystemId, SizeInBytes: SizeInBytes.Value, Status: LifeCycleState}'
