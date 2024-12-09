package main

import (
	"compare-with-robyn/config"
	"compare-with-robyn/config/db_method"
	"compare-with-robyn/routes"

	"github.com/gin-gonic/gin"
	"github.com/lpernett/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		panic("Error loading .env file")
	}

	config.InitDB()
	db_method.CreateTables()
	db_method.CreateBasePremission()

	server := gin.Default()
	routes.AuthRouter(server)
	routes.SubscribeRouter(server)
	routes.MessageRouter(server)

	server.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Hello World",
		})
	})

	server.Run(":8000")
}
