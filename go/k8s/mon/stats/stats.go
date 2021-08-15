// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements k8s mon stats manager.
package stats

import (
	"fmt"
	"regexp"
	"strings"

	"uws/log"
)

var fnre = regexp.MustCompile(`\W`)

func CleanFN(n string) string {
	fn := strings.TrimSpace(n)
	return fnre.ReplaceAllString(fn, "_")
}

type Buffer struct {
	buf *strings.Builder
}

func NewBuffer() *Buffer {
	return &Buffer{buf: new(strings.Builder)}
}

func (b *Buffer) String() string {
	return b.buf.String()
}

func (b *Buffer) Reset() {
	b.buf.Reset()
}

func (b *Buffer) Write(format string, args ...interface{}) error {
	_, err := b.buf.WriteString(fmt.Sprintf(format, args...))
	if err != nil {
		log.Error("%s", err)
	}
	return err
}

type Field struct {
	Name    string
	Label   string
	Color   int
	Draw    string
	Min     int
	Value   int64
	Unknown bool
	kind    string
}

func (f *Field) String() string {
	buf := NewBuffer()
	defer buf.Reset()
	fn := CleanFN(f.Name)
	if f.kind == "report" {
		if f.Unknown {
			buf.Write("%s.value U\n", fn)
		} else {
			buf.Write("%s.value %d\n", fn, f.Value)
		}
	} else {
		buf.Write("%s.label %s\n", fn, f.Label)
		buf.Write("%s.colour COLOUR%d\n", fn, f.Color)
		if f.Draw != "" {
			buf.Write("%s.draw %s\n", fn, f.Draw)
		}
		buf.Write("%s.min %d\n", fn, f.Min)
	}
	return buf.String()
}

type Config struct {
	Name       string
	Title      string
	Base       int
	Min        int
	Category   string
	VLabel     string
	Printf     string
	Scale      bool
	Total      string
	fields     []*Field
	fieldColor int
}

func NewConfig(name string) *Config {
	return &Config{
		Name:       name,
		Title:      "NOTITLE",
		Base:       1000,
		Min:        0,
		Category:   "NOCATEGORY",
		VLabel:     "NOLABEL",
		fields:     make([]*Field, 0),
		fieldColor: -1,
	}
}

func (c *Config) AddField(name string) *Field {
	c.fieldColor += 1
	if c.fieldColor == 29 {
		c.fieldColor = 0
	}
	f := &Field{
		Name:  name,
		Label: "NOLABEL",
		Color: c.fieldColor,
	}
	c.fields = append(c.fields, f)
	return f
}

func (c *Config) String() string {
	buf := NewBuffer()
	defer buf.Reset()
	buf.Write("multigraph %s\n", c.Name)
	buf.Write("graph_title %s\n", c.Title)
	buf.Write("graph_args --base %d -l %d\n", c.Base, c.Min)
	buf.Write("graph_category %s\n", c.Category)
	buf.Write("graph_vlabel %s\n", c.VLabel)
	if c.Printf != "" {
		buf.Write("graph_printf %s\n", c.Printf)
	}
	if c.Scale {
		buf.Write("graph_scale yes\n")
	} else {
		buf.Write("graph_scale no\n")
	}
	if c.Total != "" {
		buf.Write("graph_total %s\n", c.Total)
	}
	for _, f := range c.fields {
		buf.Write("%s", f)
	}
	return buf.String()
}

type Report struct {
	Name   string
	fields []*Field
}

func NewReport(name string) *Report {
	return &Report{
		Name:   name,
		fields: make([]*Field, 0),
	}
}

func (r *Report) AddField(name string) *Field {
	f := &Field{Name: name, kind: "report"}
	r.fields = append(r.fields, f)
	return f
}

func (r *Report) String() string {
	buf := NewBuffer()
	defer buf.Reset()
	buf.Write("multigraph %s\n", r.Name)
	for _, f := range r.fields {
		buf.Write("%s", f)
	}
	return buf.String()
}
