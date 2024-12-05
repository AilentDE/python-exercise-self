package schema

import "github.com/gin-gonic/gin"

func BaseResponseBody(message string, success bool, data interface{}, detail interface{}) gin.H {
	return gin.H{
		"success": success,
		"message": message,
		"data":    data,
		"detail":  detail,
	}
}
