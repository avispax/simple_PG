package repositories_test

import (
	"log"
	"strconv"
	"testing"
	"time"

	repo "github.com/avispax/simple_PG/GoLang2/repositories"
	"github.com/avispax/simple_PG/GoLang2/repositories/testdata"
	"github.com/stretchr/testify/assert"

	"github.com/avispax/simple_PG/GoLang2/models"
)

func TestInsertComment(t *testing.T) {

	if err := clearCommentRecord(); err != nil {
		t.Errorf("error")
		return
	}

	type args struct {
		comment models.Comment
	}
	tests := []struct {
		name    string
		args    args
		want    models.Comment
		wantErr bool
	}{
		{
			name: "1",
			args: args{
				comment: testdata.CommentTestData[0],
			},
			want:    models.Comment{},
			wantErr: false,
		},
		{
			name: "2",
			args: args{
				comment: testdata.CommentTestData[1],
			},
			want:    models.Comment{},
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repo.InsertComment(testDB, tt.args.comment)
			if (err != nil) != tt.wantErr {
				t.Errorf("InsertComment() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, tt.args.comment.ArticleID, got.ArticleID)
			assert.Equal(t, tt.args.comment.Message, got.Message)
		})
	}
}

func TestSelectCommentList(t *testing.T) {

	expect, err := initComments()
	if err != nil {
		t.Errorf("error")
		return
	}

	type args struct {
		articleID int
	}
	tests := []struct {
		name    string
		args    args
		want    []models.Comment
		wantErr bool
	}{
		{
			name: "1",
			args: args{
				articleID: 1,
			},
			want:    expect,
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repo.SelectCommentList(testDB, tt.args.articleID)
			if (err != nil) != tt.wantErr {
				t.Errorf("SelectCommentList() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, len(expect), len(got))
		})
	}
}

// clear -> insert
func initComments() ([]models.Comment, error) {
	clearCommentRecord()
	expect, err := insertCommentRecord()
	if err != nil {
		return []models.Comment{}, err
	}
	return expect, nil
}

// only clear
func clearCommentRecord() error {
	const sql = `DELETE FROM comments;`
	_, err := testDB.Exec(sql)
	if err != nil {
		return err
	}

	const sql2 = `ALTER TABLE comments auto_increment = 1;`
	_, err = testDB.Exec(sql2)
	if err != nil {
		return err
	}

	return nil
}

// only insert. 3records.
func insertCommentRecord() ([]models.Comment, error) {
	const sqlStr = `insert into comments(article_id, message, created_at) values (?,?,?);`

	comments := make([]models.Comment, 0)

	for i := 0; i < 3; i++ {
		si := strconv.Itoa(i)
		comment := models.Comment{
			ArticleID: 1,
			Message:   "msg_" + si,
			CreatedAt: time.Now(),
		}

		// SQL実行
		_, err := testDB.Exec(sqlStr, comment.ArticleID, comment.Message, comment.CreatedAt)
		if err != nil {
			log.Print(err)
			return []models.Comment{}, err
		}

		comments = append(comments, comment)
	}

	return comments, nil
}
