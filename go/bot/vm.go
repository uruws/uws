// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"context"
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
	_, err = vm.ExecuteContext(ctx, b.env.Env, opts, string(blob))
	return err
}
