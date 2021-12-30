// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"
	"regexp"
	"strconv"
	"strings"

	"uws/log"
	"uws/wapp"
)

type topPods struct {
	Namespace string `json:"namespace"`
	Name      string `json:"name"`
	CPU       uint64 `json:"cpu"`
	Mem       uint64 `json:"mem"`
}

type topPodsList struct {
	Items []topPods `json:"items"`
}

func newTopPodsList() *topPodsList {
	return &topPodsList{
		Items: make([]topPods, 0),
	}
}

var topPodsCmd string = "top pods -A --no-headers"

var reTopPods = regexp.
	MustCompile(`^(\S+)\s+(\S+)\s+([0-9]+)m\s+([0-9]+)Mi\s*$`)

func parseTopPods(l *topPodsList, out []byte) {
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			match := reTopPods.FindStringSubmatch(line)
			println(len(match))
			if len(match) == 5 {
				p := topPods{}
				p.Namespace = match[1]
				p.Name = match[2]
				p.CPU, _ = strconv.ParseUint(match[3], 10, 64)
				p.Mem, _ = strconv.ParseUint(match[4], 10, 64)
				l.Items = append(l.Items, p)
			}
		}
	}
}

func TopPods(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(topPodsCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	l := newTopPodsList()
	parseTopPods(l, out)
	wapp.WriteJSON(w, r, start, &l)
}
