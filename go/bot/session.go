// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

package bot

import (
	"net/url"
)

var _ Session = &botSession{}

type Session interface {
	SetBaseURL(string) error
	Login(string) error
}

type botSession struct {
	baseURL *url.URL
}

func (s *botSession) SetBaseURL(u string) error {
	var err error
	s.baseURL, err = url.Parse(u)
	return err
}

func (s *botSession) Login(u string) error {
	var err error
	s.baseURL, err = url.Parse(u)
	return err
}
