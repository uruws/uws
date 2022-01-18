// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"bytes"
	"net/http"
	"regexp"
	"strings"

	"uws/log"
	"uws/wapp"
)

var (
	k8sCmd = "get --raw /metrics"
	re     = regexp.MustCompile(`^([\w]+)`)
	valid  = map[string]bool{
		"aggregator_unavailable_apiservice_total":     true,
		"apiextensions_openapi_v2_regeneration_count": true,
		"apiserver_init_events_total":                 true,
		"apiserver_tls_handshake_errors_total":        true,
		"authenticated_user_requests":                 true,
		"authentication_attempts":                     true,
		"etcd_db_total_size_in_bytes":                 true,
		"go_goroutines":                               true,
		"go_info":                                     true,
		"go_memstats_alloc_bytes":                     true,
		"go_memstats_buck_hash_sys_bytes":             true,
		"go_threads":                                  true,
		"process_cpu_seconds_total":                   true,
		"process_resident_memory_bytes":               true,
		"process_virtual_memory_bytes":                true,
		"process_start_time_seconds":                  true,
	}
)

func K8s(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(k8sCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	// filter the lines we only want, to reduce network usage
	buf := new(bytes.Buffer)
	for _, line := range bytes.Split(out, []byte("\n")) {
		match := re.FindSubmatch(line)
		if len(match) > 1 {
			key := string(match[1])
			if valid[key] {
				if _, err := buf.Write(line); err != nil {
					log.DebugError(err)
					wapp.Error(w, r, start, err)
					return
				}
				buf.WriteString("\n")
			}
		}
	}
	wapp.Write(w, r, start, "%s", buf.Bytes())
}
