// vscode の機能で ctrl + shift + p -> Go:Generate Unit Test for File

package repositories_test

import (
	"database/sql"
	"fmt"
	"reflect"
	"testing"

	"github.com/avispax/simple_PG/GoLang2/models"
	"github.com/avispax/simple_PG/GoLang2/repositories"

	_ "github.com/go-sql-driver/mysql"
)

func TestInsertArticles(t *testing.T) {
	type args struct {
		db      *sql.DB
		article models.Article
	}
	tests := []struct {
		name    string
		args    args
		want    models.Article
		wantErr bool
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repositories.InsertArticles(tt.args.db, tt.args.article)
			if (err != nil) != tt.wantErr {
				t.Errorf("InsertArticles() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("InsertArticles() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSelectArticleList(t *testing.T) {
	type args struct {
		db   *sql.DB
		page int
	}
	tests := []struct {
		name    string
		args    args
		want    []models.Article
		wantErr bool
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := repositories.SelectArticleList(tt.args.db, tt.args.page)
			if (err != nil) != tt.wantErr {
				t.Errorf("SelectArticleList() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("SelectArticleList() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestSelectArticleDetail(t *testing.T) {
	// 上記の構造体で色々やるのも面倒だったので、ここでいったん定義する。
	dbConn := fmt.Sprintf("%s:%s@tcp(127.0.0.1:3306)/%s?parseTime=true", "docker",
		"docker", "sampledb")
	db, err := sql.Open("mysql", dbConn)
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()

	type args struct {
		db        *sql.DB
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
				db:        nil,
				articleId: 1,
			},
			want: models.Article{
				ID:       1,
				Title:    "firstPost",
				Contents: "This is my first blog",
				UserName: "saki",
				NiceNum:  3,
			},
			wantErr: false,
		},
		{
			name: "2",
			args: args{
				db:        nil,
				articleId: 2,
			},
			want: models.Article{
				ID:       2,
				Title:    "se",
				Contents: "second",
				UserName: "omy",
				NiceNum:  4,
			},
			wantErr: false,
		},
		{
			name: "3",
			args: args{
				db:        nil,
				articleId: 3,
			},
			want: models.Article{
				ID:       3,
				Title:    "title3",
				Contents: "contents3",
				UserName: "username3",
				NiceNum:  0,
			},
			wantErr: false,
		},
	}
	for _, tt := range tests {

		t.Run(tt.name, func(t *testing.T) {

			tt.args.db = db // で、付け替える。

			// ここから generator 通り。
			got, err := repositories.SelectArticleDetail(tt.args.db, tt.args.articleId)
			if (err != nil) != tt.wantErr {
				t.Errorf("SelectArticleDetail() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if got.ID != tt.want.ID {
				t.Errorf("id : get %d but want %d\n", got.ID, tt.want.ID)
			}

			if got.Title != tt.want.Title {
				t.Errorf("Title : get %s but want %s\n", got.Title, tt.want.Title)
			}

			if got.Contents != tt.want.Contents {
				t.Errorf("Contents : get %s but want %s\n", got.Contents, tt.want.Contents)
			}

			if got.UserName != tt.want.UserName {
				t.Errorf("UserName : get %s but want %s\n", got.UserName, tt.want.UserName)
			}

			if got.NiceNum != tt.want.NiceNum {
				t.Errorf("NiceNum : get %d but want %d\n", got.NiceNum, tt.want.NiceNum)
			}

			// if !reflect.DeepEqual(got, tt.want) {
			// 	t.Errorf("SelectArticleDetail() = %v, want %v", got, tt.want)
			// }
		})
	}
}

func TestUpdateNiceNum(t *testing.T) {
	type args struct {
		db        *sql.DB
		articleId int
	}
	tests := []struct {
		name    string
		args    args
		wantErr bool
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := repositories.UpdateNiceNum(tt.args.db, tt.args.articleId); (err != nil) != tt.wantErr {
				t.Errorf("UpdateNiceNum() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}
