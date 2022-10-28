package main

import (
	"fmt"
	"myGo/mypkg"
)

// 別パッケージは go module(go.mod)を使うとラク。
func myFunc1() {

	aaa := mypkg.MyStruct{111, 222}
	fmt.Println(aaa.GetField1())
	fmt.Println(aaa.GetField2())

}

func main() {
	myFunc1() // 別パッケージもの

}
