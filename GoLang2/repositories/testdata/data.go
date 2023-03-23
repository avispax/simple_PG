package testdata

import "github.com/avispax/simple_PG/GoLang2/models"

var ArticleTestData = []models.Article{
	models.Article{
		ID:       1,
		Title:    "firstPost",
		Contents: "This is my first blog",
		UserName: "saki",
		NiceNum:  2,
	},
	models.Article{
		ID:       2,
		Title:    "2nd",
		Contents: "Second blog post",
		UserName: "saki",
		NiceNum:  4,
	},
}

var CommentTestData = []models.Comment{
	models.Comment{
		ArticleID: 1,
		Message:   "aaa",
	},
	models.Comment{
		ArticleID: 1,
		Message:   "bbb",
	},
}
