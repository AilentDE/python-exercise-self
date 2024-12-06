package middlewares

import (
	"compare-with-robyn/logic/schema"
	"compare-with-robyn/utils"
	"net/http"

	"github.com/gin-gonic/gin"
)

func RequireAuthenticator(ctx *gin.Context) {
	token := ctx.GetHeader("Authorization")
	if token == "" {
		ctx.AbortWithStatusJSON(http.StatusUnauthorized, schema.BaseResponseBody("Unauthorized", false, nil, nil))
		ctx.Abort()
		return
	}

	payload, err := utils.DecideAccessToken(&token)
	if err != nil {
		ctx.AbortWithStatusJSON(http.StatusUnauthorized, schema.BaseResponseBody("Unauthorized", false, nil, err.Error()))
		ctx.Abort()
		return
	}

	ctx.Set("userId", payload.Id)
	ctx.Set("userName", payload.Username)
	ctx.Next()
}

func OptionAuthenticator(ctx *gin.Context) {
	token := ctx.GetHeader("Authorization")
	if token == "" {
		ctx.Set("userId", "")
		ctx.Set("userName", "")
		ctx.Next()
		return
	}

	payload, err := utils.DecideAccessToken(&token)
	if err != nil {
		ctx.AbortWithStatusJSON(http.StatusUnauthorized, schema.BaseResponseBody("Unauthorized", false, nil, err.Error()))
		ctx.Abort()
		return
	}

	ctx.Set("userId", payload.Id)
	ctx.Set("userName", payload.Username)
	ctx.Next()
}
