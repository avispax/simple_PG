package main

import (
	"fmt"
	"log"
	"net/http"
	"net/url"

	"github.com/avispax/simple_PG/GoLang2/handlers"
	// "github.com/avispax/simple_PG/GoLang2/models"

	"github.com/gorilla/mux"
)

func main() {

	// myFunc1()
	// myFunc2()
	myFunc()

}

func myFunc1() {
	// sample
	u, _ := url.Parse("http://localhost:8080?page=1&page=2&a=1&")
	queryMap := u.Query()

	fmt.Println(queryMap["page"])
	m2 := queryMap["page"]
	fmt.Println(m2[1])
	fmt.Println(queryMap["a"])

	fmt.Println(queryMap["b"])

}

// func myFunc2() {

// 	comment1 := models.Comment{
// 		CommentID: 1,
// 		ArticleID: 1,
// 		Message:   "Comment Message 1",
// 		CreatedAt: time.Now(),
// 	}

// 	comment2 := models.Comment{
// 		CommentID: 2,
// 		ArticleID: 1,
// 		Message:   "Comment Message 2",
// 		CreatedAt: time.Now(),
// 	}

// 	article := models.Article{
// 		ID:          1,
// 		Title:       "Article 1",
// 		Contents:    "Article Contents 1",
// 		NiceNum:     0,
// 		CommentList: []models.Comment{comment1, comment2},
// 		CreatedAt:   time.Now(),
// 	}
// 	jsonData, err := json.Marshal(article)
// 	if err != nil {
// 		fmt.Println(err)
// 		return
// 	}
// 	fmt.Printf("%s\n", jsonData)
// }

func myFunc() {
	// ルーター定義
	r := mux.NewRouter()

	// ハンドラ登録
	r.HandleFunc("/hello", handlers.HelloHandler).Methods(http.MethodGet) // アドレスと紐づくハンドラ、影響するHttpメソッドをこの1文で定義。
	r.HandleFunc("/article", handlers.PostArticleHandler).Methods(http.MethodPost)
	r.HandleFunc("/article/list", handlers.ArticleListHandler).Methods(http.MethodGet)
	r.HandleFunc("/article/{id:[0-9]+}", handlers.ArticleDetailHandler).Methods(http.MethodGet)
	r.HandleFunc("/article/nice", handlers.PostNiceHandler).Methods(http.MethodPost)
	r.HandleFunc("/comment", handlers.PostCommentHandler).Methods(http.MethodPost)

	log.Println("Server start at port 8080.")  // ただのログ
	log.Fatal(http.ListenAndServe(":8080", r)) // サーバー起動

}
