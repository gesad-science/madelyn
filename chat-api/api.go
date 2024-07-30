package main

import (
  "log"
  "os"
  "time"
  "fmt"

  "github.com/joho/godotenv"
  tele "gopkg.in/telebot.v3"
  // "github.com/gomodule/redigo/redis"
)


func main() {
    // Checking dotenv
    err := godotenv.Load(".env")
    if err != nil {
	log.Fatalf("Error loading .env file: %s", err)
    }

    // Connecting to Valkey
    //conn, err := redis.Dial("tcp", "valkey:6379"); // fix connection to docker network
    //if err != nil {
    //  log.Fatal(err);
    //}
    
    // Assuring connection is closed
    //defer conn.Close();

    // bot preferences
    pref := tele.Settings{
	Token: os.Getenv("TOKEN"),
	Poller: &tele.LongPoller{Timeout: 10 * time.Second},
    }

    b, err := tele.NewBot(pref) // initializing a new bot
    if err != nil {
	log.Fatal(err)
	return
    }

    // Setting up a hello command
    b.Handle("/hello", func(c tele.Context) error {
	return c.Send("Hello FOCIONA, BITCH!!!!!")
    });
    
    b.Handle(tele.OnText, func(c tele.Context) error {
    	//result, err := redis.StringMap(conn.Do("HGETALL",  "album:1"));
	user := c.Sender();
	chat := c.Chat();
	message := fmt.Sprintf("Mama mia user is %s and chat is %d", user.Username, chat.ID);
	return c.Send(message);
    });

    b.Handle("/start", func(c tele.Context) error {
	return c.Send("Start here")
    })
    
    // Bootstraping the bot server
    b.Start()
}
