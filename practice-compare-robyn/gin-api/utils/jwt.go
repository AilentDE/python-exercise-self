package utils

import (
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var ALGORITHM = os.Getenv("ALGORITHM")
var SECRET_KEY = os.Getenv("SECRET_KEY")

type AuthPayload struct {
	Id       string `json:"id"`
	Username string `json:"username"`
}

func (payload *AuthPayload) CreateAccessToken() (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"id":       payload.Id,
		"username": payload.Username,
		"exp":      time.Now().Add(time.Minute * 30).Unix(),
		"iat":      time.Now().Unix(),
	})

	return token.SignedString([]byte(SECRET_KEY))
}

func DecideAccessToken(token string) (AuthPayload, error) {
	parsedToken, err := jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		_, ok := token.Method.(*jwt.SigningMethodHMAC)
		if !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return []byte(SECRET_KEY), nil
	})
	if err != nil {
		return AuthPayload{}, err
	}

	tokenValid := parsedToken.Valid
	if !tokenValid {
		return AuthPayload{}, jwt.ErrSignatureInvalid
	}

	claims, ok := parsedToken.Claims.(jwt.MapClaims)
	if !ok {
		return AuthPayload{}, jwt.ErrSignatureInvalid
	}

	return AuthPayload{
		Id:       claims["id"].(string),
		Username: claims["username"].(string),
	}, nil
}
