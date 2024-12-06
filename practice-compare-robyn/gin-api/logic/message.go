package logic

import (
	"compare-with-robyn/logic/schema"
	"compare-with-robyn/models"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type userOutput struct {
	id       string
	username string
	email    string
}

type messageCreated struct {
	ID              string `json:"id"`
	AuthorId        string `json:"authorId"`
	Title           string `json:"title"`
	Content         string `json:"content"`
	PermissionLevel uint8  `json:"permissionLevel"`
	CreatedAt       string `json:"createdAt"`
	UpdatedAt       string `json:"updatedAt"`
}

func CreateMessage(ctx *gin.Context) {
	var message models.Message
	var err error
	userId := ctx.GetString("userId")

	err = ctx.ShouldBindJSON(&message)
	message.AuthorID = uuid.MustParse(userId)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	err = message.Create()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	outputMessage := messageCreated{
		ID:              message.ID.String(),
		AuthorId:        message.AuthorID.String(),
		Title:           message.Title,
		Content:         message.Content,
		PermissionLevel: message.PermissionLevel,
		CreatedAt:       message.CreatedAt.UTC().Format("2006-01-02T15:04:05.999999999Z"),
		UpdatedAt:       message.UpdatedAt.UTC().Format("2006-01-02T15:04:05.999999999Z"),
	}
	ctx.JSON(http.StatusCreated, schema.BaseResponseBody("Message created successfully", true, outputMessage, nil))
}

func DeleteMessage(ctx *gin.Context) {
	var err error
	messageId := ctx.Param("messageId")
	userId := ctx.GetString("userId")

	message := models.Message{
		ID:       uuid.MustParse(messageId),
		AuthorID: uuid.MustParse(userId),
	}
	err = message.Delete()
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
	}

	ctx.JSON(http.StatusOK, schema.BaseResponseBody("Message deleted successfully", true, map[string]string{
		"messageId": messageId,
	}, nil))
}
