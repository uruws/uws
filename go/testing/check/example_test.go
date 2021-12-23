// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package check_test

import (
	"fmt"
	"testing"

	. "uws/testing/check"
)

func ExampleFatal() {
	t := new(testing.T)
	fmt.Println(Fatal(t, IsNil(t, nil, "check param")))

	// Output:
	// true
}

func ExampleIsEqual() {
	t := new(testing.T)
	fmt.Println(IsEqual(t, 1, 1, "error info"))

	// Output:
	// true
}

func ExampleNotEqual() {
	t := new(testing.T)
	fmt.Println(NotEqual(t, "a", "b", "error info"))

	// Output:
	// true
}

// If you need to do some post fail tasks you can check the exit status of the
// condition.
func Example_postFail() {
	t := new(testing.T)

	if NotEqual(t, "a", "b", "error info") {
		fmt.Println("failed")

		// t.Errorf was already called by NotEqual so the test was already
		// marked as failed and a message was logged.

		// So no need to do that. But you may want to call t.FailNow() to abort
		// execution if Fatal can not by used because some steps are needed
		// between the condition failed and aborting execution.

		// Or anything else.
	}

	// Output:
	// failed
}
