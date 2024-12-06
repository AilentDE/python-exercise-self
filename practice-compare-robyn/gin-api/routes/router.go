package routes

import (
	"github.com/gin-gonic/gin"

	"compare-with-robyn/logic"
	"compare-with-robyn/middlewares"
)

func AuthRouter(server *gin.Engine) {
	authRouter := server.Group("/auth")
	authRouter.POST("/login", logic.LoginUser)
	authRouter.POST("/register", logic.RegisterUser)
}

func SubscribeRouter(server *gin.Engine) {
	subscribeRouter := server.Group("/subscribe")
	subscribeRouter.Use(middlewares.RequireAuthenticator)
	subscribeRouter.POST("/:userId/join", logic.SubscribeUser)
	subscribeRouter.POST("/:userId/withdraw", logic.UnsubscribeUser)
}

func MessageRouter(server *gin.Engine) {
	messageRouter := server.Group("/message")
	messageRouter.POST("/create", middlewares.RequireAuthenticator, logic.CreateMessage)
	messageRouter.DELETE("/:messageId/delete", middlewares.RequireAuthenticator, logic.DeleteMessage)
	messageRouter.GET("/:messageId", middlewares.OptionAuthenticator, func(c *gin.Context) {})
	messageRouter.GET("/:messageId/auth", middlewares.OptionAuthenticator, func(c *gin.Context) {})

	messagesRouter := server.Group("/messages")
	messagesRouter.Use(middlewares.RequireAuthenticator)
	messagesRouter.GET("/", func(c *gin.Context) {})
	messagesRouter.GET("/auth", func(c *gin.Context) {})

	server.GET("/history", middlewares.RequireAuthenticator, func(c *gin.Context) {})
}
