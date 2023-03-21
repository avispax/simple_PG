package handlers

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"strconv"

	"github.com/avispax/simple_PG/GoLang2/models"
	"github.com/gorilla/mux"
)

func HelloHandler(w http.ResponseWriter, req *http.Request) {
	io.WriteString(w, "Hello World!!\n")
}

func PostArticleHandler(w http.ResponseWriter, req *http.Request) {

	// リクエストのBodyから投稿内容をJSONで読み込む
	var reqArticle models.Article
	if err := json.NewDecoder(req.Body).Decode(&reqArticle); err != nil {
		http.Error(w, "fail to decode json.\n", http.StatusBadRequest)
		return
	}

	// 読み込んだJSONを構造体に格納する。
	article := reqArticle
	json.NewEncoder(w).Encode(article)
}

func ArticleListHandler(w http.ResponseWriter, req *http.Request) {
	queryMap := req.URL.Query()

	var page int                                     // 何ページ目を指定してきたのかを格納する変数。
	if p, ok := queryMap["page"]; ok && len(p) > 0 { // page指定があればよし。（複数の場合は最初のやつを採用）
		var err error
		page, err = strconv.Atoi(p[0]) // ここで 0番目の配列を採用。（複数の場合は最初のやつ）
		if err != nil {
			http.Error(w, "Invalid query Parameter", http.StatusBadRequest) // 数値じゃないならこっち（page=xxxみたいなのはこっち）
			return
		}
	} else {
		// page指定がなければ1ページ目限定
		page = 1
	}

	log.Println(page)

	articleList := []models.Article{models.Article1, models.Article2}
	json.NewEncoder(w).Encode(articleList)
}

func ArticleDetailHandler(w http.ResponseWriter, req *http.Request) {
	articleId, err := strconv.Atoi(mux.Vars(req)["id"])
	if err != nil {
		http.Error(w, "Invalid query Parameter.", http.StatusBadRequest)
		return
	}

	log.Println(articleId)

	article := models.Article1
	json.NewEncoder(w).Encode(article)

}

func PostNiceHandler(w http.ResponseWriter, req *http.Request) {
	// テスト用
	var reqArticle models.Article

	if err := json.NewDecoder(req.Body).Decode(&reqArticle); err != nil {
		http.Error(w, "fail to decode json.\n", http.StatusBadRequest)
		return
	}

	article := models.Article1
	json.NewEncoder(w).Encode(article)

}

func PostCommentHandler(w http.ResponseWriter, req *http.Request) {

	var reqArticle models.Article
	if err := json.NewDecoder(req.Body).Decode(&reqArticle); err != nil {
		log.Println(err)
		http.Error(w, "fail to decode json.\n", http.StatusBadRequest)
		return
	}

	article := models.Article1
	json.NewEncoder(w).Encode(article)
}
