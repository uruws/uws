// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"errors"
	"os"
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)


var (
	bupKubeOutFH func(string, string) (*os.File, error)
	bupKubeErrFH func(string, string) (*os.File, error)
)

func init() {
	bupKubeOutFH = kubeOutFH
	bupKubeErrFH = kubeErrFH
}

func mockTempFileError(d, f string) (*os.File, error) {
	return nil, errors.New("mock_error")
}

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

func TestKubeOutFHError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubeOutFH = mockTempFileError
	defer func() {
		kubeOutFH = bupKubeOutFH
	}()
	_, err := Kube("testing")
	NotNil(t, err, "kube error")
	IsEqual(t, err.Error(), "mock_error", "error message")
}

func TestKubeErrFHError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubeErrFH = mockTempFileError
	defer func() {
		kubeErrFH = bupKubeErrFH
	}()
	_, err := Kube("testing")
	NotNil(t, err, "kube error")
	IsEqual(t, err.Error(), "mock_error", "error message")
}
