// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-job-stats cmd.
package main

import (
	"flag"
	"fmt"
	"os"
	"strings"

	"uws/api/job/stats"
	"uws/log"
)

func main() {
	log.Init("api-job-stats")

	db_name := strings.TrimSpace(os.Getenv("MONGO_DB_NAME"))
	if db_name == "" {
		log.Fatal("MONGO_DB_NAME not set")
	}
	db_uri := strings.TrimSpace(os.Getenv("MONGO_DB_URI"))
	if db_uri == "" {
		log.Fatal("MONGO_DB_URI not set")
	}

	env := strings.TrimSpace(os.Getenv("api_env"))
	if env == "" {
		env = "default"
	}
	flag.StringVar(&env, "env", env, "env `name`")

	flag.Parse()

	var err error

	cmd := flag.Arg(0)
	st := stats.New(db_name, db_uri)

	if cmd == "config" {
		err = st.Config()
		if err == nil {
			err = Config(st, env)
		}
	} else {
		cmd = "report"
		if errcount := st.Fetch(); errcount > 0 {
			err = log.NewError("fetch failed with %d error(s)", errcount)
		}
		if err == nil {
			err = Report(st, env)
		}
	}

	if err != nil {
		log.Fatal("stats %s: %s", cmd, err)
	}
}

func getColour(i int) (int, string) {
	if i > 28 {
		i = 0
	}
	n := fmt.Sprintf("COLOUR%d", i)
	return i + 1, n
}

// Config generates munin plugin config output.
func Config(st *stats.Stats, env string) error {
	log.Debug("config: %d", st.Len())

	fmt.Printf("multigraph apijob_%s\n", env)
	fmt.Printf("graph_title %s api jobs\n", env)
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel seconds")
	fmt.Println("graph_category apijob")
	fmt.Println("graph_scale no")
	fmt.Println("f0_total.label number of jobs")
	fmt.Println("f0_total.colour COLOUR0")
	fmt.Println("f0_total.min 0")
	fmt.Println("f1_errors.label job number of errors")
	fmt.Println("f1_errors.colour COLOUR0")
	fmt.Println("f1_errors.min 0")

	fmt.Printf("multigraph apijob_%s_elapsed_time\n", env)
	fmt.Printf("graph_title %s api jobs stats elapsed time\n", env)
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel seconds")
	fmt.Println("graph_category apijob")
	fmt.Println("graph_scale yes")
	col := 0
	coln := ""
	for _, job := range st.List() {
		fmt.Printf("%s.label %s took\n", job.ID, job.Label)
		col, coln = getColour(col)
		fmt.Printf("%s.colour %s\n", job.ID, coln)
		fmt.Printf("%s.min 0\n", job.ID)
	}

	for _, job := range st.List() {
		fmt.Printf("multigraph apijob_%s.%s\n", env, job.ID)
		fmt.Printf("graph_title %s api %s\n", env, job.Name)
		fmt.Println("graph_args --base 1000 -l 0")
		fmt.Println("graph_vlabel number of")
		fmt.Println("graph_category api")
		fmt.Println("graph_scale no")
		fmt.Println("f0_ready.label ready")
		fmt.Println("f0_ready.colour COLOUR0")
		fmt.Println("f0_ready.min 0")
		fmt.Println("f1_running.label running")
		fmt.Println("f1_running.colour COLOUR1")
		fmt.Println("f1_running.min 0")
		fmt.Println("f2_failed.label failed")
		fmt.Println("f2_failed.colour COLOUR2")
		fmt.Println("f2_failed.min 0")
	}
	return nil
}

// Report prints munin plugin values.
func Report(st *stats.Stats, env string) error {
	log.Debug("report: %d", st.Len())

	total := 0
	errors := 0
	fmt.Printf("multigraph apijob_%s\n", env)
	for _, job := range st.List() {
		total += 1
		if job.Error != nil {
			errors += 1
		}
	}
	fmt.Printf("f0_total.value %d\n", total)
	fmt.Printf("f1_errors.value %d\n", errors)

	fmt.Printf("multigraph apijob_%s_elapsed_time\n", env)
	for _, job := range st.List() {
		if job.Error != nil {
			fmt.Printf("%s.value %d\n", job.ID, job.Took)
		} else {
			fmt.Printf("%s.value U\n", job.ID)
		}
	}

	for _, job := range st.List() {
		fmt.Printf("multigraph apijob_%s.%s\n", env, job.ID)
		if job.Error != nil {
			fmt.Printf("f0_ready.value %d\n", job.Ready)
			fmt.Printf("f1_running.value %d\n", job.Running)
			fmt.Printf("f2_failed.value %d\n", job.Failed)
		} else {
			fmt.Println("f0_ready.value U")
			fmt.Println("f1_running.value U")
			fmt.Println("f2_failed.value U")
		}
	}
	return nil
}
