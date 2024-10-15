package db

import (
  "fmt"
  "database/sql"

  _ "github.com/lib/pq"
)

type PostgresConfig struct {
  user string
  password string
  host string
  dbName string
  sslMode string
  connURI string
}

func NewConfig(user string, password string, host string, dbName string) PostgresConfig {
  pc := PostgresConfig{
    user:       user,
    password:   password,
    host:       host,
    sslMode:    "verify-full",
    dbName:     dbName,
  }

  return pc
}

func (pc PostgresConfig) SetURI() PostgresConfig {
  pc.connURI = fmt.Sprintf(
    "postgres://%s:%s@%s/%s?sslmode=%s",
    pc.user, pc.password, pc.host, pc.dbName, pc.sslMode
  )

  return pc
}

func NewPostgresStorage(cfg PostgresConfig) (db *sql.DB, error) {

  
  
}
