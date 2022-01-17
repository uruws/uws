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
	Count   uint   `json:"count"`
	CPU     uint64 `json:"cpu"`
	CPUMin  uint64 `json:"cpu_min"`
	CPUMax  uint64 `json:"cpu_max"`
	CPUP    uint   `json:"cpup"` // percentage
	CPUPMin uint   `json:"cpup_min"`
	CPUPMax uint   `json:"cpup_max"`
	Mem     uint64 `json:"mem"`
	MemMin  uint64 `json:"mem_min"`
	MemMax  uint64 `json:"mem_max"`
	MemP    uint   `json:"memp"` // percentage
	MemPMin uint   `json:"memp_min"`
	MemPMax uint   `json:"memp_max"`
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
				cpup64, _ := strconv.ParseUint(match[2], 10, 32)
				cpup := uint(cpup64)
				mem, _ := strconv.ParseUint(match[3], 10, 64)
				memp64, _ := strconv.ParseUint(match[4], 10, 32)
				memp := uint(memp64)
				if ! minSet {
					tn.CPUMin = cpu
					tn.CPUPMin = cpup
					tn.MemMin = mem
					tn.MemPMin = memp
					minSet = true
				}
				tn.CPU += cpu
				if cpu < tn.CPUMin {
					tn.CPUMin = cpu
				}
				if cpu > tn.CPUMax {
					tn.CPUMax = cpu
				}
				tn.CPUP += cpup
				if cpup < tn.CPUPMin {
					tn.CPUPMin = cpup
				}
				if cpup > tn.CPUPMax {
					tn.CPUPMax = cpup
				}
				tn.Mem += mem
				if mem < tn.MemMin {
					tn.MemMin = mem
				}
				if mem > tn.MemMax {
					tn.MemMax = mem
				}
				tn.MemP += memp
				if memp < tn.MemPMin {
					tn.MemPMin = memp
				}
				if memp > tn.MemPMax {
					tn.MemPMax = memp
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
