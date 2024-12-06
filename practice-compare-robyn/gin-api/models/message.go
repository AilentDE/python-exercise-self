package models

import (
	"compare-with-robyn/config"
	"errors"
	"fmt"

	"github.com/google/uuid"
)

type MessagePremission struct {
	ID          uuid.UUID `gorm:"type:uuid;primaryKey;default:uuid_generate_v4()"`
	Level       uint8     `gorm:"not null;unique"`
	Description string    `gorm:"default:''"`
}

type Message struct {
	ID                uuid.UUID `gorm:"type:uuid;primaryKey;default:uuid_generate_v4()"`
	AuthorID          uuid.UUID `gorm:"type:uuid;not null"`
	Title             string
	Content           string
	PermissionLevel   uint8             `gorm:"not null" json:"permission_level"`
	User              User              `gorm:"foreignKey:AuthorID;constraint:OnDelete:SET NULL"`
	MessagePremission MessagePremission `gorm:"foreignKey:PermissionLevel;references:Level"`
	MixinTime
}

type ReadHistory struct {
	ID        uuid.UUID `gorm:"type:uuid;primaryKey;default:uuid_generate_v4()"`
	UserID    uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_user_message"`
	MessageID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_user_message"`
	User      User      `gorm:"foreignKey:UserID"`
	Message   Message   `gorm:"foreignKey:MessageID;constraint:OnDelete:CASCADE"`
	MixinTime
}

func BasePremission() []MessagePremission {
	return []MessagePremission{
		{Level: 1, Description: "Public"},
		{Level: 2, Description: "Protected"},
		{Level: 3, Description: "Private"},
	}
}

func (m *Message) Create() error {
	return config.DB.Create(m).Error
}

func (m *Message) Delete() error {
	return config.DB.Where("author_id = ?", m.AuthorID).Delete(m).Error
}

func (m *Message) Find(userId string) (Message, User, error) {

	if userId == "" {
		var result struct {
			Message
			User
		}

		err := config.DB.Model(m).Select("messages.*, users.*").Joins("JOIN users ON messages.author_id = users.id").Where("messages.id = ? AND messages.permission_level = ?", m.ID, 0).First(&result).Error
		if err != nil {
			return Message{}, User{}, err
		}

		return result.Message, result.User, nil
	} else {
		var subResult struct {
			Message
			User
			SubscriptionID *uuid.UUID `gorm:"column:subscription_id"`
		}

		err := config.DB.Model(m).Select("messages.*, users.*, user_subscriptions.id AS subscription_id").Joins("JOIN users ON messages.author_id = users.id").Joins("LEFT JOIN user_subscriptions ON user_subscriptions.author_id = messages.author_id AND user_subscriptions.user_id = ?", uuid.MustParse(userId)).Where("messages.id = ?", m.ID).First(&subResult).Error
		if err != nil {
			return Message{}, User{}, err
		}

		if subResult.Message.AuthorID == uuid.MustParse(userId) {
			return subResult.Message, subResult.User, nil
		} else if subResult.Message.PermissionLevel == 2 || (subResult.Message.PermissionLevel == 1 && subResult.SubscriptionID == nil) {
			return Message{}, User{}, errors.New("Premission denied")
		}
		return subResult.Message, subResult.User, nil
	}
}

func (m *Message) All(userId string, skip int, limit int) ([]struct {
	Message
	User
}, error) {
	var results []struct {
		Message
		User
	}
	var searchPremission = []uint8{0, 1}

	stmt := config.DB.Model(m).Select("messages.*, users.*").Joins("JOIN users ON messages.author_id = users.id").Offset(skip).Limit(limit).Order("messages.created_at desc")
	if userId != "" {
		err := stmt.Where("messages.permission_level IN (?) OR messages.author_id = ?", searchPremission, uuid.MustParse(userId)).Find(&results).Error
		if err != nil {
			return nil, err
		}
	} else {
		err := stmt.Where("messages.permission_level IN (?)", searchPremission).Find(&results).Error
		if err != nil {
			return nil, err
		}
	}
	for _, message := range results {
		fmt.Println("message", message.Message)
		fmt.Println("user", message.User)
	}
	return results, nil
}
