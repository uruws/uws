// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"

	. "uws/testing/check"
)

func TestDeployCmd(t *testing.T) {
	IsEqual(t, deployCmd, "get deployments,statefulset,daemonset -A -o json", "deploy cmd")
}
