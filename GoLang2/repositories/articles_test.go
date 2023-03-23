// vscode の機能で ctrl + shift + p -> Go:Generate Unit Test for File

package repositories_test

import (
	"fmt"
	"log"
	"strconv"
	"testing"
	"time"

	"github.com/avispax/simple_PG/GoLang2/models"
	"github.com/avispax/simple_PG/GoLang2/repositories"
	"github.com/avispax/simple_PG/GoLang2/repositories/testdata"
	"github.com/stretchr/testify/assert"

	_ "github.com/go-sql-driver/mysql"
)

func TestInsertArticles(t *testing.T) {

	// 初期処理。DBを空っぽに。
	if err := clearArticleRecord(); err != nil {
		t.Fatalf("clear Error")
		return
	}

	// test
	tests := []struct {
		name    string
		want    models.Article
		wantErr bool
	}{
		{
			name:    "1",
			want:    testdata.ArticleTestData[0],
			wantErr: false,
		},
		{
			name:    "2",
			want:    testdata.ArticleTestData[1],
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repositories.InsertArticles(testDB, tt.want)
			if (err != nil) != tt.wantErr {
				t.Errorf("InsertArticles() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, tt.want.ID, got.ID)
			assert.Equal(t, tt.want.Contents, got.Contents)
			assert.Equal(t, tt.want.UserName, got.UserName)
			assert.Equal(t, 0, got.NiceNum)
		})
	}
}

func TestSelectArticleList(t *testing.T) {
	// 初期処理。
	expect, err := initArticles()
	if err != nil {
		t.Fatalf("init Error")
		return
	}

	type args struct {
		page int
	}
	tests := []struct {
		name    string
		args    args
		want    []models.Article
		wantErr bool
	}{
		{
			name: "1",
			args: args{
				page: 1,
			},
			want:    expect,
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repositories.SelectArticleList(testDB, tt.args.page)
			if (err != nil) != tt.wantErr {
				t.Errorf("SelectArticleList() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, len(got), len(tt.want))
		})
	}
}

func TestSelectArticleDetail(t *testing.T) {
	// 初期処理。
	expect, err := initArticles()
	if err != nil {
		t.Fatalf("init Error")
		return
	}

	type args struct {
		articleId int
	}
	tests := []struct {
		name    string
		args    args
		want    models.Article
		wantErr bool
	}{
		{
			name: "1",
			args: args{
				articleId: 1,
			},
			want:    expect[0],
			wantErr: false,
		},
		{
			name: "2",
			args: args{
				articleId: 2,
			},
			want:    expect[1],
			wantErr: false,
		},
		{
			name: "3",
			args: args{
				articleId: 3,
			},
			want:    expect[2],
			wantErr: false,
		},
	}
	for _, tt := range tests {

		t.Run(tt.name, func(t *testing.T) {

			got, err := repositories.SelectArticleDetail(testDB, tt.args.articleId)
			if (err != nil) != tt.wantErr {
				t.Errorf("SelectArticleDetail() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			// check
			assert.Equal(t, tt.want.ID, got.ID)
			assert.Equal(t, tt.want.Title, got.Title)
			assert.Equal(t, tt.want.Contents, got.Contents)
			assert.Equal(t, tt.want.UserName, got.UserName)
			assert.Equal(t, tt.want.NiceNum, got.NiceNum)
			// assert.Equal(t, tt.want.CreatedAt, got.CreatedAt)
		})
	}
}

func TestUpdateNiceNum(t *testing.T) {
	// 初期処理。
	expect, err := initArticles()
	if err != nil {
		t.Fatalf("init Error")
		return
	}

	type args struct {
		articleId int
	}
	tests := []struct {
		name    string
		args    args
		want    models.Article
		wantErr bool
	}{
		{
			name: "1",
			args: args{
				articleId: 1,
			},
			want:    expect[0],
			wantErr: false,
		},
		{
			name: "2",
			args: args{
				articleId: 99,
			},
			want:    expect[1],
			wantErr: true,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := repositories.UpdateNiceNum(testDB, tt.args.articleId); (err != nil) != tt.wantErr {
				t.Errorf("UpdateNiceNum() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

// clear -> insert
func initArticles() ([]models.Article, error) {
	if err := clearArticleRecord(); err != nil {
		return []models.Article{}, err
	}

	expect, err := insertArticleRecord()
	if err != nil {
		return []models.Article{}, err
	}
	return expect, nil
}

// only clear
func clearArticleRecord() error {
	const sql0 = `DELETE FROM comments;`
	_, err := testDB.Exec(sql0)
	if err != nil {
		fmt.Println(err)
		return err
	}

	const sql = `DELETE FROM articles;`
	_, err = testDB.Exec(sql)
	if err != nil {
		fmt.Println(err)
		return err
	}

	const sql2 = `ALTER TABLE articles auto_increment = 1;`
	_, err = testDB.Exec(sql2)
	if err != nil {
		fmt.Println(err)
		return err
	}

	return nil
}

// only insert. 3records.
func insertArticleRecord() ([]models.Article, error) {
	const sqlStr = `insert into articles(title, contents, username, nice, created_at) values (?,?,?,?,?);`

	articles := make([]models.Article, 0)

	for i := 0; i < 3; i++ {
		si := strconv.Itoa(i)
		article := models.Article{
			ID:        i + 1,
			Title:     "title_" + si,
			Contents:  "content_" + si,
			UserName:  "username_" + si,
			NiceNum:   i,
			CreatedAt: time.Now(),
		}

		// SQL実行
		_, err := testDB.Exec(sqlStr, article.Title, article.Contents, article.UserName, i, article.CreatedAt)
		if err != nil {
			log.Print(err)
			return []models.Article{}, err
		}

		articles = append(articles, article)
	}

	return articles, nil
}
