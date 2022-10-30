package myTst

import (
	"testing"
)

func TestIsOne_001(t *testing.T) {
	n := 1
	b := IsOne(n)

	if !b {
		t.Errorf("%d is not 1", n)
	}
}

func TestIsOne_002(t *testing.T) {
	n := 2
	b := IsOne(n)

	if b {
		t.Errorf("%d is not 1", n)
	}
}
