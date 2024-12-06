package logic

import (
	"compare-with-robyn/logic/schema"
	"compare-with-robyn/models"
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type userOutput struct {
	ID       string `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
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

type messageOutput struct {
	ID              string     `json:"id"`
	Author          userOutput `json:"author"`
	Title           string     `json:"title"`
	Content         string     `json:"content"`
	PermissionLevel uint8      `json:"permissionLevel"`
	CreatedAt       string     `json:"createdAt"`
	UpdatedAt       string     `json:"updatedAt"`
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

func GetMessage(ctx *gin.Context) {
	userId := ctx.GetString("userId")
	messageId := ctx.Param("messageId")
	parsedMessageId, err := uuid.Parse(messageId)
	if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody("Message not found", false, nil, err.Error()))
		return
	}

	message := models.Message{
		ID: parsedMessageId,
	}
	foundMessage, messageAuthor, err := message.Find(userId)
	if errors.Is(err, gorm.ErrRecordNotFound) {
		ctx.JSON(http.StatusOK, schema.BaseResponseBody("Message not found", true, nil, err.Error()))
		return
	} else if err != nil {
		ctx.JSON(http.StatusBadRequest, schema.BaseResponseBody(err.Error(), false, nil, nil))
		return
	}

	outputMessage := messageOutput{
		ID: foundMessage.ID.String(),
		Author: userOutput{
			ID:       messageAuthor.ID.String(),
			Username: messageAuthor.UserName,
			Email:    messageAuthor.Email,
		},
		Title:           foundMessage.Title,
		Content:         foundMessage.Content,
		PermissionLevel: foundMessage.PermissionLevel,
		CreatedAt:       foundMessage.CreatedAt.UTC().Format("2006-01-02T15:04:05.999999999Z"),
		UpdatedAt:       foundMessage.UpdatedAt.UTC().Format("2006-01-02T15:04:05.999999999Z"),
	}
	ctx.JSON(http.StatusOK, schema.BaseResponseBody("Get message successfully", true, outputMessage, nil))
}
