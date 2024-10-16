package config

import (
 "os"
 "fmt"
 "github.com/joho/godotenv"
) 

type PostgresConfig struct {
	user     string
	password string
	host     string
	port     string
	dbName   string
	sslMode  string
	ConnURI  string
}

var PGConfig = NewPGConfig().SetURI()

func NewPGConfig() PostgresConfig {
  godotenv.Load()
	return PostgresConfig{
		user:         getEnv("PG_USER", "postgres"),
		password:     getEnv("POSTGRES_PASSWORD", "secret"),
		host:         getEnv("PG_HOST", "localhost"),
		port:         getEnv("PG_PORT", "5432"),
		sslMode:      getEnv("SSLMODE", "disable"),
		dbName:       getEnv("DB", "postgres"),
	}
}

func (pc PostgresConfig) SetURI() PostgresConfig {
	pc.ConnURI = fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=%s", pc.user, pc.password, pc.host, pc.port, pc.dbName, pc.sslMode)
	return pc
}

func getEnv(key, defaultValue string) string {
  if value, ok := os.LookupEnv(key); ok {
    return value
  }

  return defaultValue
}
