// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"errors"
	"io"
	"os"
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)


var (
	develKubecmd     string
	bupKubecmd       string
	bupKubeOutFH     func(string, string) (*os.File, error)
	bupKubeErrFH     func(string, string) (*os.File, error)
	bupKubeSeekOutFH func(io.Seeker) error
	bupKubeSeekErrFH func(io.Seeker) error
	bupKubeReadAllFH func(io.Reader) ([]byte, error)
)

func init() {
	develKubecmd = "/go/src/uws/k8s/mon/_devel/uwskube.sh"
	bupKubecmd = kubecmd
	bupKubeOutFH = kubeOutFH
	bupKubeErrFH = kubeErrFH
	bupKubeSeekOutFH = kubeSeekOutFH
	bupKubeSeekErrFH = kubeSeekErrFH
	bupKubeReadAllFH = kubeReadAllFH
}

func mockTempFileError(d, f string) (*os.File, error) {
	return nil, errors.New("mock_error")
}

func mockSeekFHError(fh io.Seeker) error {
	return errors.New("mock_error")
}

func mockReadAllFHError(fh io.Reader) ([]byte, error) {
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

func TestKubeSeekOutFHError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	kubeSeekOutFH = mockSeekFHError
	defer func() {
		kubecmd = bupKubecmd
		kubeSeekOutFH = bupKubeSeekOutFH
	}()
	_, err := Kube("testing")
	NotNil(t, err, "kube error")
	IsEqual(t, err.Error(), "mock_error", "error message")
}

func TestKubeSeekErrFHError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubeSeekErrFH = mockSeekFHError
	defer func() {
		kubeSeekErrFH = bupKubeSeekErrFH
	}()
	_, err := Kube("testing")
	NotNil(t, err, "kube error")
	Match(t, "errfh seek: mock_error$", mock.LoggerOutput(), "log output")
}

func TestKubeErrorOutput(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	defer func() {
		kubecmd = bupKubecmd
	}()
	_, err := Kube("test_error_output")
	NotNil(t, err, "kube error")
	Match(t, "\\[ERROR\\] mock_error$", mock.LoggerOutput(), "log output")
}

func TestKubeErrorOutputReadError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	kubeReadAllFH = mockReadAllFHError
	defer func() {
		kubecmd = bupKubecmd
		kubeReadAllFH = bupKubeReadAllFH
	}()
	_, err := Kube("test_error_output")
	NotNil(t, err, "kube error")
	Match(t, "\\[ERROR\\] errfh read: mock_error$", mock.LoggerOutput(), "log output")
}
