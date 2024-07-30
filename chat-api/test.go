package main


import (
    "os"
    "log"
    "fmt"
    "github.com/joho/godotenv"
)


func main() {
    
    err := godotenv.Load(".env")
    if err != nil {
	log.Fatalf("Error loading .env: %s", err)
	return
    }

    fmt.Println(os.Getenv("TOKEN"))
}
