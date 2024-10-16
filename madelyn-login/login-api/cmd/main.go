package main

import (
	"log"
	"database/sql"
	
  "github.com/gesad-science/login-api/cmd/api"
	"github.com/gesad-science/login-api/db"
	"github.com/gesad-science/login-api/config"
)

func main() {
	db, err := db.NewPostgresStorage(config.PGConfig)
  if err != nil {
    log.Fatal(err)
  }
  
	initStorage(db)
  defer db.Close()

  server := api.NewAPIServer(":8000", nil)
	if err := server.Run(); err != nil {
		log.Fatal(err)
	}
}

func initStorage(db *sql.DB) {
  if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

  log.Println("[ POSTGRES ] - users batabase: Successfully connected")
}
