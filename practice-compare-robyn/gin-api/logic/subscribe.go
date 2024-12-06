package logic

import (
	"compare-with-robyn/logic/schema"
	"compare-with-robyn/models"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func SubscribeUser(ctx *gin.Context) {
	var err error
	targetId := ctx.Param("userId")
	userId := ctx.GetString("userId")

	subscribe := models.UserSubscription{
		UserID:   uuid.MustParse(userId),
		AuthorID: uuid.MustParse(targetId),
	}
	err = subscribe.Create()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	ctx.JSON(http.StatusOK, schema.BaseResponseBody("User subscribed successfully", true, map[string]string{
		"target": targetId,
	}, nil))
}

func UnsubscribeUser(ctx *gin.Context) {
	var err error
	targetId := ctx.Param("userId")
	userId := ctx.GetString("userId")

	subscribe := models.UserSubscription{
		UserID:   uuid.MustParse(userId),
		AuthorID: uuid.MustParse(targetId),
	}
	err = subscribe.Delete()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	ctx.JSON(http.StatusOK, schema.BaseResponseBody("User unsubscribed successfully", true, map[string]string{
		"target": targetId,
	}, nil))
}
