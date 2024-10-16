package db

import (
	"database/sql"
	"log"

	"github.com/gesad-science/login-api/config"
	_ "github.com/lib/pq"
)

func NewPostgresStorage(cfg config.PostgresConfig) (db *sql.DB, err error) {
	db, err = sql.Open("postgres", cfg.ConnURI)
	if err != nil {
		log.Fatal(err)
	}

	return db, nil
}
