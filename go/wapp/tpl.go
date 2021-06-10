// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package wapp

import (
	"html/template"
	"path/filepath"

	"uws/log"
)

var baseTpl *template.Template

func LoadTemplates(tpldir string) error {
	log.Debug("load templates")
	var err error
	baseFn := filepath.Join(tpldir, "base.html")
	baseTpl, err = template.New("base").ParseFiles(baseFn)
	if err != nil {
		return log.DebugError(err)
	}
	log.Debug("load templates done!")
	return nil
}
