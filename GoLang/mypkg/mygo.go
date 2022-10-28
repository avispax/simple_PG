package mypkg

type MyStruct struct {
	Field1 int
	Field2 int
}

func (g *MyStruct) GetField1() int {
	return g.Field1
}

func (g *MyStruct) GetField2() int {
	return g.Field2
}
