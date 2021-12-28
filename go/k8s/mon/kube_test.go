// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)

func TestKubeCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	_, err := Kube("testing")
	NotNil(t, err, "kube error")
	IsEqual(t, err.Error(),
		"fork/exec /usr/local/bin/uwskube: no such file or directory",
		"kube error message")
	IsEqual(t, mock.LoggerOutput(), "", "log output")
}
