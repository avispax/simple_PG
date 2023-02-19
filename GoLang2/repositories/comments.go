package repositories

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/avispax/simple_PG/GoLang2/models"
)

func InsertComment(db *sql.DB, comment models.Comment) (models.Comment, error) {
	const sqlStr = `INSERT INTO comments(article_id, message, created_at) VALUES (?, ?, now());`

	result, err := db.Exec(sqlStr, comment.ArticleID, comment.Message)
	if err != nil {
		log.Fatal(err)
		return models.Comment{}, err
	}

	var newComment models.Comment
	newComment.ArticleID, newComment.Message = comment.ArticleID, comment.Message

	id, _ := result.LastInsertId()
	newComment.CommentID = int(id)

	fmt.Println(result.LastInsertId())
	fmt.Println(result.RowsAffected())

	return newComment, nil
}

func SelectCommentList(db *sql.DB, articleID int) ([]models.Comment, error) {
	const sqlStr = `select * from comments where article_id = ?`

	rows, err := db.Query(sqlStr, articleID)
	if err != nil {
		log.Fatal(err)
		return nil, err
	}
	defer rows.Close()

	comments := make([]models.Comment, 0)
	for rows.Next() {
		var comment models.Comment
		var createdTime sql.NullTime

		if err := rows.Scan(&comment.ArticleID, &comment.CommentID, &comment.Message, &createdTime); err != nil {
			log.Fatal(err)
			return nil, err
		}

		if createdTime.Valid {
			comment.CreatedAt = createdTime.Time
		}
		comments = append(comments, comment)
	}

	return comments, nil
}
