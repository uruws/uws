#!/bin/sh
set -eu

pl_ena=/root/bin/plugin-enable.sh

${pl_ena} contrib docker/docker_ docker_containers
${pl_ena} contrib docker/docker_ docker_cpu
${pl_ena} contrib docker/docker_ docker_images
${pl_ena} contrib docker/docker_ docker_memory
${pl_ena} contrib docker/docker_ docker_network
${pl_ena} contrib docker/docker_ docker_status
${pl_ena} contrib docker/docker_ docker_volumes

exit 0
