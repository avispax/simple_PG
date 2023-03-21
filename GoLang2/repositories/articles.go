package repositories

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/avispax/simple_PG/GoLang2/models"
)

const (
	articleNumPerPage = 5
)

// 新規投稿をデータベースに insert する関数
// -> データベースに保存した記事内容と、発生したエラーを返り値にする
func InsertArticles(db *sql.DB, article models.Article) (models.Article, error) {
	const sqlStr = `insert into articles(title, contents, username, nice, created_at) values (?,?,?,0,now());`

	// SQL実行
	result, err := db.Exec(sqlStr, article.Title, article.Contents, article.UserName)
	if err != nil {
		log.Fatal(err)
		return models.Article{}, err
	}

	var newArticle models.Article
	newArticle.Title, newArticle.Contents, newArticle.UserName = article.Title, article.Contents, article.UserName

	id, _ := result.LastInsertId()
	newArticle.ID = int(id)

	fmt.Println(result.LastInsertId())
	fmt.Println(result.RowsAffected())

	return newArticle, nil
}

func SelectArticleList(db *sql.DB, page int) ([]models.Article, error) {
	const sqlStr = `select article_id, title, contents, username, nice from articles limit ? offset ?;`

	// SQL 実行 複数件の場合はQueryを使う
	rows, err := db.Query(sqlStr, articleNumPerPage, ((page - 1) * articleNumPerPage))
	if err != nil {
		log.Fatal(err)
		return nil, err
	}
	defer rows.Close()

	articles := make([]models.Article, 0)
	for rows.Next() {
		var article models.Article
		rows.Scan(&article.ID, &article.Title, &article.Contents, &article.UserName, &article.NiceNum)
		articles = append(articles, article)
	}

	return articles, nil
}

func SelectArticleDetail(db *sql.DB, articleId int) (models.Article, error) {
	const sqlStr = `select * from articles where article_id = ?;`

	// SQL実行 1件確定のレコードはQueryRowを使う。ID指定のときなど。
	row := db.QueryRow(sqlStr, articleId)
	if err := row.Err(); err != nil {
		log.Fatal(err)
		return models.Article{}, err
	}

	var article models.Article
	var createdTime sql.NullTime
	if err := row.Scan(&article.ID, &article.Title, &article.Contents, &article.UserName, &article.NiceNum, &createdTime); err != nil {
		log.Fatal(err)
		return models.Article{}, err
	}

	if createdTime.Valid {
		article.CreatedAt = createdTime.Time
	}

	return article, nil
}

func UpdateNiceNum(db *sql.DB, articleId int) error {
	const sqlGetNice = `SELECT nice from articles where article_id = ?;`

	row := db.QueryRow(sqlGetNice, articleId)
	if err := row.Err(); err != nil {
		log.Fatal(err)
		return err
	}

	var niceNum int
	if err := row.Scan(&niceNum); err != nil {
		log.Fatal(err)
		return err
	}

	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
		return err
	}

	const sqlUpdateNice = `UPDATE articles SET nice = ? WHERE article_id = ?;`
	result, err := db.Exec(sqlUpdateNice, niceNum+1, articleId)
	if err != nil {
		tx.Rollback()
		log.Fatal(err)
		return err
	}

	fmt.Println(result.LastInsertId())
	fmt.Println(result.RowsAffected())

	if err := tx.Commit(); err != nil {
		log.Fatal(err)
		return err
	}
	return nil
}
