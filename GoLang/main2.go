package main

import (
	"fmt"
	"myGo/myTst"
	"myGo/mypkg"
	"reflect"
	"strconv"
)

// 別パッケージは go module(go.mod)を使うとラク。
func myFunc1() {

	aaa := mypkg.MyStruct{111, 222}
	fmt.Println(aaa.GetField1())
	fmt.Println(aaa.GetField2())

}

type Point struct {
	x int
	y int
}

func myFunc2() {

	ps := make([]Point, 5)
	for _, p := range ps {
		fmt.Println(p.x, p.y)
	}

}

type Points []*Point

func myFunc3() {
	ps := Points{}
	ps = append(ps, &Point{x: 1, y: 2})
	ps = append(ps, &Point{x: 888, y: 999})
	// fmt.Println(ps) // 別に何がしたいわけでもない

	fmt.Println(reflect.TypeOf(ps))

	for i, v := range ps {
		fmt.Println(i, v)
	}
}

type MyError struct {
	Message string
	ErrCode int
}

// インターフェイスの実装 適当な構造体でもError() が実装されてりゃ error インターフェイスの実態になり得るってこと？
func (e *MyError) Error() string {
	return e.Message
}

func RaiseError() error {
	// error 型としてOKになってる理由は、ひとつ上の関数で Error() string を実装したから
	// それがあることこそが error らしい
	return &MyError{Message: "myError やで", ErrCode: 999}
}

func myFunc4() {
	// 慣れたら java の interface と似ているところもある
	err := RaiseError()
	fmt.Println(err.Error())
}

// ここから5
type Stringify interface {
	MyString() string
}

type MyStruct1 struct {
	Name string
	Age  int
}

func (s *MyStruct1) MyString() string {
	return fmt.Sprintf("%s(%d)", s.Name, s.Age)
}

type MyStruct2 struct {
	Number string
	Model  string
}

func (s *MyStruct2) MyString() string {
	return fmt.Sprintf("%s : %s", s.Number, s.Model)
}

func myFunc5() {

	vs := []Stringify{
		&MyStruct1{Name: "Taro", Age: 21},
		&MyStruct2{Number: "MyNumber1", Model: "MyModel1"},
	}

	for _, v := range vs {
		fmt.Println(v.MyString())
	}
}

// 5から続けて6
func myPrintln(s Stringify) { // Stringify が interface じゃけんね。
	fmt.Println(s.MyString())
}

func myFunc6() {
	myPrintln(&MyStruct1{Name: "Suzuki", Age: 99}) // MyStructはStringifyの実装してるから、この関数のinterface部分も行ける。
	myPrintln(&MyStruct2{Number: "num001", Model: "model001"})
}

// 7
type MyIF interface {
	MyFunc7_1() string
	MyFunc7_2() string
}

type MyIF2 interface {
	MyFunc72() string
}

type MyStruct71 struct {
	Id   int
	Name string
}

func (s *MyStruct71) MyFunc7_1() string {
	return fmt.Sprintf("7_1 : %d : %s", s.Id, s.Name)
}

func (s *MyStruct71) MyFunc7_2() string {
	return fmt.Sprintf("7_2 : %d : %s", s.Id, s.Name)
}

func (s *MyStruct71) MyFunc72() string {
	return fmt.Sprintf("72 : %d : %s", s.Id, s.Name)
}

func myFunc71_2(i MyIF) {
	fmt.Println(i.MyFunc7_1())
	fmt.Println(i.MyFunc7_2())
}

func myFunc7() {
	m71_1 := &MyStruct71{Id: 1, Name: "71太郎"}
	fmt.Println(m71_1.MyFunc7_1()) // 多重IF、OK
	fmt.Println(m71_1.MyFunc7_2()) // 多重IF、OK
	fmt.Println(m71_1.MyFunc72())

	myFunc71_2(m71_1) // 多重IFのインスタンスを関数にアレしてもOK。ただし、この場合は「MyIF」のみ使用可能MyIF2は無理。
}

func myFunc8() {

	if myTst.IsOne(1) {
		fmt.Println("8 : true")
	}
}

func myFunc9() {
	data := "hello"
	b := []byte(data) // cast
	fmt.Println(b)
	fmt.Println(string(b)) // cast

}

func myFunc10() {
	var limit int32 = 10000
	var offset int32 = 0

	fmt.Println("result_" + strconv.Itoa(int(offset)) + "_" + strconv.Itoa(int(limit)) + ".txt")

}

func myFunc11() {
	i := 0
	for i < 10 {
		fmt.Println(i)
		i++
	}
}

func myFunc12_1(n *int) int {
	// get next char です。
	*n++

	// if *n == 34 {
	// 	*n = 35
	// } else if *n == 40 {
	// 	*n = 42
	// } else if *n == 44 {
	// 	*n = 45
	// } else if *n == 46 {
	// 	*n = 47
	// } else if *n == 58 {
	// 	*n = 61
	// } else if *n == 62 {
	// 	*n = 63
	// } else if *n == 64 {
	// 	*n = 65
	// } else if *n == 91 {
	// 	*n = 94
	// } else if *n == 127 {
	// 	*n = -1
	// }

	if *n == 128 {
		*n = -1
	}

	return *n
}

func myFunc12() {

	for n := 32; n < 128; n++ {
		// fmt.Println(string(n))
		fmt.Println(fmt.Sprint(n))
	}

	// s := "0123456789"
	// s += "abcdefghijklmnopqrstuvwxyz"
	// s += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	// s += "!#$%&'*+-/=?^_`{|}~"

}

func myFunc13() {

	aaa := "aiueo"
	bbb := map[string]int{"apple": 150, "banana": 300, "lemon": 300}
	fmt.Println(fmt.Errorf("%s deleted records exists.%+v", aaa, bbb))

}

func main() {
	// myFunc1() // 別パッケージもの
	// myFunc2() // 構造体
	// myFunc3() // 構造体2
	// myFunc4() // インターフェイス : error
	// myFunc5() // インターフェイス2
	// myFunc6() // インターフェイス3
	// myFunc7() // インターフェイス4 : 多重実装行けるか？
	// myFunc8() // テスト関連

	// myFunc9() // []byte と string
	// myFunc10() // なんか文字列操作 result_int32.txtみたいな。
	// myFunc11() // for の終了条件だけでOKかどうか。
	// myFunc12() // ascii 使えるかどうか
	myFunc13() // ログ

}
