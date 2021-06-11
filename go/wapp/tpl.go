// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package wapp

import (
	"html/template"
	"path/filepath"

	"uws/log"
)

var tpls map[string]*template.Template

func init() {
	tpls = make(map[string]*template.Template)
}

func LoadTemplates(tpldir, appdir string) error {
	if err := loadBaseTemplates(tpldir); err != nil {
		return err
	}
	log.Debug("load templates done!")
	return nil
}

func loadBaseTemplates(tpldir string) error {
	log.Debug("load base templates")

	fn := filepath.Join(tpldir, "base.html")
	tpl, err := template.New("base.html").ParseFiles(fn)
	if err != nil {
		return log.DebugError(err)
	}
	tpls["base.html"] = tpl

	fn = filepath.Join(tpldir, "error.html")
	tpl, err = template.New("error.html").ParseFiles(fn)
	if err != nil {
		return log.DebugError(err)
	}
	tpls["error.html"] = tpl

	return nil
}
