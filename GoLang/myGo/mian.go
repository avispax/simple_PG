package main

import (
	"fmt"
	"myGo/mypkg"
)

func myFunc1() {

	aaa := mypkg.MyStruct{111, 222}
	fmt.Println(aaa.GetField1())
	fmt.Println(aaa.GetField2())

}

func main() {
	myFunc1() // 別パッケージもの

}
