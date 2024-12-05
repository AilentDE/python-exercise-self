package logic

import (
	"compare-with-robyn/logic/schema"
	"compare-with-robyn/models"
	"net/http"

	"github.com/gin-gonic/gin"
)

func RegisterUser(ctx *gin.Context) {
	var user models.User
	var err error

	err = ctx.ShouldBindJSON(&user)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	err = user.Create()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	token, error := user.GetAccessToken()
	if error != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	ctx.JSON(http.StatusCreated, schema.BaseResponseBody("User created successfully", true, map[string]string{"accessToken": token}, nil))
}

func LoginUser(ctx *gin.Context) {
	var user models.User
	var err error

	err = ctx.ShouldBindJSON(&user)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	err = user.ValidateCerdentials()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	token, error := user.GetAccessToken()
	if error != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	ctx.JSON(http.StatusOK, schema.BaseResponseBody("User logged in successfully", true, map[string]string{"accessToken": token}, nil))
}
