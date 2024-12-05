package routes

import (
	"github.com/gin-gonic/gin"

	"compare-with-robyn/logic"
)

func AuthRouter(server *gin.Engine) {
	authRouter := server.Group("/auth")
	authRouter.POST("/login", logic.LoginUser)
	authRouter.POST("/register", logic.RegisterUser)
}

func SubscribeRouter(server *gin.Engine) {
	subscribeRouter := server.Group("/subscribe")
	subscribeRouter.POST("/:userId/join", func(c *gin.Context) {})
	subscribeRouter.POST("/:userId/withdraw", func(c *gin.Context) {})
}

func MessageRouter(server *gin.Engine) {
	messageRouter := server.Group("/message")
	messageRouter.POST("/create", func(c *gin.Context) {})
	messageRouter.DELETE("/:messageId/delete", func(c *gin.Context) {})
	messageRouter.GET("/:messageId", func(c *gin.Context) {})
	messageRouter.GET("/:messageId/auth", func(c *gin.Context) {})

	messagesRouter := server.Group("/messages")
	messagesRouter.GET("/", func(c *gin.Context) {})
	messagesRouter.GET("/auth", func(c *gin.Context) {})

	server.GET("/history", func(c *gin.Context) {})
}
