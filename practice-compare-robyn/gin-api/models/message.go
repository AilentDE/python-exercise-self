package models

import "github.com/google/uuid"

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
	PremissionLevel   uint8             `gorm:"not null"`
	User              User              `gorm:"foreignKey:AuthorID;constraint:OnDelete:SET NULL"`
	MessagePremission MessagePremission `gorm:"foreignKey:PremissionLevel"`
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
