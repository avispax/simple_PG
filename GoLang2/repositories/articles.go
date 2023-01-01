package repositories

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/avispax/simple_PG/GoLang2/models"
)

// 新規投稿をデータベースに insert する関数
// -> データベースに保存した記事内容と、発生したエラーを返り値にする
func InsertArticles(db *sql.DB, article models.Article) (models.Article, error) {
	const sqlStr = `insert into articles(title, contents, username, nice, created_at) values (?,?,?,0,now());`

	// TODO: aaa
	result, err := db.Exec(sqlStr, article.Title, article.Connect, article.UserName)
	if err != nil {
		log.Fatal(err)
		return nil, err
	}
	fmt.Println(result.LastInsertId())
	fmt.Println(result.RowsAffected())

	return result, nil
}
