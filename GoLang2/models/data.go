package models

import "time"

var (
	Comment1 = Comment{
		CommentID: 1,
		ArticleID: 1,
		Message:   "test message 1",
		CreatedAt: time.Now(),
	}

	Comment2 = Comment{
		CommentID: 2,
		ArticleID: 1,
		Message:   "test message 2",
		CreatedAt: time.Now(),
	}
)

var (
	Article1 = Article{
		ID:          1,
		Title:       "title 1",
		Contents:    "contents 1",
		UserName:    "UserName1",
		NiceNum:     0,
		CommentList: []Comment{Comment1, Comment2},
		CreatedAt:   time.Now(),
	}

	Article2 = Article{
		ID:        1,
		Title:     "title 2",
		Contents:  "contents 2",
		UserName:  "UserName 2",
		NiceNum:   200,
		CreatedAt: time.Now(),
	}
)
