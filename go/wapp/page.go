// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package wapp

type Page struct {
	tplBase string
	tplName string
	Title   string
}

func NewPage(tpl string) *Page {
	return &Page{tplBase: "base.html", tplName: tpl}
}
