// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"context"
	"fmt"
	"io/ioutil"

	"github.com/mattn/anko/vm"

	"uws/log"
)

var opts *vm.Options

func init() {
	opts = &vm.Options{Debug: true}
}

func vmExec(ctx context.Context, b *Bot, filename string) error {
	log.Debug("execute: %s", filename)
	blob, err := ioutil.ReadFile(filename)
	if err != nil {
		return err
	}
	var exit interface{}
	exit, err = vm.ExecuteContext(ctx, b.env.Env, opts, string(blob))
	if exit != nil {
		return fmt.Errorf("%s: %s", filename, exit)
	}
	return err
}
