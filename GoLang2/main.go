package main

import (
	"log"
	"net/http"

	"github.com/avispax/simple_PG/GoLang2/handlers"

	"github.com/gorilla/mux"
)

func main() {
	// ルーター定義
	r := mux.NewRouter()
	// ハンドラ登録
	r.HandleFunc("/hello", handlers.HelloHandler).Methods(http.MethodGet)
	r.HandleFunc("/article", handlers.PostArticleHandler).Methods(http.MethodPost)
	r.HandleFunc("/article/list", handlers.ArticleListHandler).Methods(http.MethodGet)
	r.HandleFunc("/article/{id:[0-9]+}", handlers.ArticleDetailHandler).Methods(http.MethodGet)
	r.HandleFunc("/article/nice", handlers.PostNiceHandler).Methods(http.MethodPost)
	r.HandleFunc("/comment", handlers.PostCommentHandler).Methods(http.MethodPost)

	log.Println("Server start at port 8080.")  // ただのログ
	log.Fatal(http.ListenAndServe(":8080", r)) // サーバー起動

}
