// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/url"
	"time"

	"uws/config"
	"uws/log"
)

var _ Session = &botSession{}

type Session interface {
	SetBaseURL(string) error
	Login(string) error
	Logout(string) error
	Get(string) (*http.Response, error)
}

type botSession struct {
	baseURL   string
	auth      bool
	authToken string
	userId    string
	cli       *http.Client
	script    string
}

func newBotSession() *botSession {
	cli := new(http.Client)
	cli.Timeout = 5 * time.Minute
	return &botSession{cli: cli}
}

func (s *botSession) setScript(n string) {
	s.script = n
}

func (s *botSession) SetBaseURL(u string) error {
	x, err := url.Parse(u)
	if err != nil {
		return err
	}
	s.baseURL = x.String()
	return nil
}

type respData struct {
	AuthToken string `json:"authToken"`
	UserId    string `json:"userId"`
}

type loginResponse struct {
	Status string    `json:"status"`
	Data   *respData `json:"data"`
}

func (s *botSession) getCredentials() url.Values {
	cfg := config.NewUserConfig()
	if err := cfg.Load("bot", "credentials.yml"); err != nil {
		log.Error("%s", err)
	}
	e := cfg.Get("e")
	if e == "" {
		e = "NOEMAIL"
	}
	p := cfg.Get("p")
	if p == "" {
		p = "NOPASSWD"
	}
	return url.Values{"email": {e}, "password": {p}}
}

func (s *botSession) Login(u string) error {
	var (
		resp *http.Response
		err  error
	)
	req := newPostFormRequest(s.script, s.baseURL+u, s.getCredentials())
	if s.auth {
		return log.Error("bot is already logged in!")
	}
	resp, err = s.cli.Do(req)
	if err != nil {
		return err
	}
	//~ log.Debug("resp %v", resp)
	if resp.StatusCode != http.StatusOK {
		return log.Error("login invalid response status code: %d", resp.StatusCode)
	}
	ctype := resp.Header.Get("content-type")
	if ctype != "application/json" {
		return log.Error("login invalid response content type: %s", ctype)
	}
	defer resp.Body.Close()
	blob, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return log.Error("login read response: %s", err)
	}
	body := &loginResponse{Data: new(respData)}
	if err := json.Unmarshal(blob, &body); err != nil {
		return log.Error("login response body: %s", err)
	}
	if body.Status != "success" {
		return log.Error("login response body status: %s", body.Status)
	}
	if body.Data.AuthToken == "" {
		return log.Error("login response body empty auth token")
	}
	if body.Data.UserId == "" {
		return log.Error("login response body empty user id")
	}
	s.authToken = body.Data.AuthToken
	s.userId = body.Data.UserId
	s.auth = true
	return nil
}

type logoutResponse struct {
	Status string `json:"status"`
}

func (s *botSession) Logout(u string) error {
	var (
		resp *http.Response
		err  error
	)
	req := newPostFormRequest(s.script, s.baseURL+u, nil)
	if s.auth {
		requestAuth(req, s.authToken, s.userId)
	}
	resp, err = s.cli.Do(req)
	if err != nil {
		return err
	}
	//~ log.Debug("resp: %v", resp)
	if resp.StatusCode != http.StatusOK {
		return log.Error("logout invalid response status code: %d", resp.StatusCode)
	}
	ctype := resp.Header.Get("content-type")
	if ctype != "application/json" {
		return log.Error("logout invalid response content type: %s", ctype)
	}
	defer resp.Body.Close()
	blob, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return log.Error("logout read response: %s", err)
	}
	body := &logoutResponse{}
	if err := json.Unmarshal(blob, &body); err != nil {
		return log.Error("logout response body: %s", err)
	}
	if body.Status != "success" {
		return log.Error("logout response body status: %s", body.Status)
	}
	return nil
}

func (s *botSession) Get(u string) (*http.Response, error) {
	req := newGetRequest(s.script, s.baseURL+u)
	if s.auth {
		requestAuth(req, s.authToken, s.userId)
	}
	return s.cli.Do(req)
}

func (s *botSession) PostForm(u string, v url.Values) (*http.Response, error) {
	req := newPostFormRequest(s.script, s.baseURL+u, v)
	if s.auth {
		requestAuth(req, s.authToken, s.userId)
	}
	defer func() {
		if req.Body != nil {
			req.Body.Close()
		}
	}()
	return s.cli.Do(req)
}

func (s *botSession) PostJSON(u string, v string) (*http.Response, error) {
	req := newPostJSONRequest(s.script, s.baseURL+u, v)
	if s.auth {
		requestAuth(req, s.authToken, s.userId)
	}
	defer func() {
		if req.Body != nil {
			req.Body.Close()
		}
	}()
	return s.cli.Do(req)
}
