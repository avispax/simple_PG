package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"

	"github.com/avispax/simple_PG/GoLang2/models"
	"github.com/gorilla/mux"
)

func HelloHandler(w http.ResponseWriter, req *http.Request) {
	io.WriteString(w, "Hello World!!\n")
}

func PostArticleHandler(w http.ResponseWriter, req *http.Request) {
	article := models.Article1
	jsonData, err := json.Marshal(article)
	if err != nil {
		http.Error(w, "fail to encode json\n", http.StatusInternalServerError)
		return
	}
	w.Write(jsonData)
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

	// resString := fmt.Sprintf("Article List (page %d)\n", page)
	// io.WriteString(w, resString)

	// テスト用
	articleList := []models.Article{models.Article1, models.Article2}
	jsonData, err := json.Marshal(articleList)
	if err != nil {
		errMsg := fmt.Sprintf("fail to encode json(page %d)\n", page)
		http.Error(w, errMsg, http.StatusInternalServerError)
		return
	}

	w.Write(jsonData)
}

func ArticleDetailHandler(w http.ResponseWriter, req *http.Request) {
	articleId, err := strconv.Atoi(mux.Vars(req)["id"])
	if err != nil {
		http.Error(w, "Invalid query Parameter.", http.StatusBadRequest)
		return
	}
	// resString := fmt.Sprintf("Article No. %d\n", articleId)
	// io.WriteString(w, resString)

	// テスト用
	article := models.Article1
	jsonData, err := json.Marshal(article)
	if err != nil {
		errMsg := fmt.Sprintf("fail to encode json(articleID %d)\n", articleId)
		http.Error(w, errMsg, http.StatusInternalServerError)
		return
	}

	w.Write(jsonData)

}

func PostNiceHandler(w http.ResponseWriter, req *http.Request) {
	// テスト用
	article := models.Article1
	jsonData, err := json.Marshal(article)
	if err != nil {
		http.Error(w, "fail to encode json.\n", http.StatusInternalServerError)
		return
	}

	w.Write(jsonData)
}

func PostCommentHandler(w http.ResponseWriter, req *http.Request) {
	// テスト用
	article := models.Article1
	jsonData, err := json.Marshal(article)
	if err != nil {
		http.Error(w, "fail to encode json.\n", http.StatusInternalServerError)
		return
	}

	w.Write(jsonData)
}
