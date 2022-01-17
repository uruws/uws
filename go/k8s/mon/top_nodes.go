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

type topNodes struct {
	Count  uint   `json:"count"`
	CPU    uint64 `json:"cpu"`
	CPUP   uint   `json:"cpup"` // percentage
	CPUMin uint64 `json:"cpu_min"`
	CPUMax uint64 `json:"cpu_max"`
	Mem    uint64 `json:"mem"`
	MemP   uint   `json:"memp"` // percentage
	MemMin uint64 `json:"mem_min"`
	MemMax uint64 `json:"mem_max"`
}

var topNodesCmd string = "top nodes --no-headers"

var reTopNodes = regexp.
	MustCompile(`^\S+\s+([0-9]+)m\s+([0-9]+)%\s+([0-9]+)Mi\s+([0-9]+)%\s*$`)

func parseTopNodes(tn *topNodes, out []byte) error {
	minSet := false
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			match := reTopNodes.FindStringSubmatch(line)
			if len(match) == 5 {
				cpu, _ := strconv.ParseUint(match[1], 10, 64)
				cpup, _ := strconv.ParseUint(match[2], 10, 32)
				mem, _ := strconv.ParseUint(match[3], 10, 64)
				memp, _ := strconv.ParseUint(match[4], 10, 32)
				if ! minSet {
					tn.CPUMin = cpu
					tn.MemMin = mem
					minSet = true
				}
				tn.CPU += cpu
				tn.CPUP += uint(cpup)
				if cpu < tn.CPUMin {
					tn.CPUMin = cpu
				}
				if cpu > tn.CPUMax {
					tn.CPUMax = cpu
				}
				tn.Mem += mem
				tn.MemP += uint(memp)
				if mem < tn.MemMin {
					tn.MemMin = mem
				}
				if mem > tn.MemMax {
					tn.MemMax = mem
				}
				tn.Count++
			}
		}
	}
	return nil
}

func TopNodes(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(topNodesCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	tn := new(topNodes)
	parseTopNodes(tn, out)
	wapp.WriteJSON(w, r, start, &tn)
}
