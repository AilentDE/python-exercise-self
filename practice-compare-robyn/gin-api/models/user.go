package models

import (
	"compare-with-robyn/config"
	"compare-with-robyn/utils"
	"errors"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm/clause"
)

type User struct {
	ID       uuid.UUID `gorm:"type:uuid;primaryKey;default:uuid_generate_v4()"`
	UserName string    `gorm:"unique;not null;index"`
	Password string    `gorm:"not null"`
	Email    string    `gorm:"unique;not null"`
	MixinTime
}

type UserSubscription struct {
	ID       uuid.UUID `gorm:"type:uuid;primaryKey;default:uuid_generate_v4()"`
	UserID   uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_user_author"`
	AuthorID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_user_author"`
	User     User      `gorm:"foreignKey:UserID;constraint:OnDelete:SET NULL"`
	Author   User      `gorm:"foreignKey:AuthorID;constraint:OnDelete:SET NULL"`
	MixinTime
}

func (u *User) Create() error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.Password = string(hashedPassword)

	err = config.DB.Create(u).Error
	if err != nil {
		return err
	}
	return nil
}

func (u *User) ValidateCerdentials() error {
	var findedUser User

	err := config.DB.First(&findedUser, "user_name = ?", u.UserName).Error
	if err != nil {
		return errors.New("user not found")
	}

	err = bcrypt.CompareHashAndPassword([]byte(findedUser.Password), []byte(u.Password))
	if err != nil {
		return errors.New("password is incorrect")
	}

	return nil
}

func (u *User) GetAccessToken() (string, error) {
	auth := utils.AuthPayload{
		Id:       u.ID.String(),
		Username: u.UserName,
	}
	token, err := auth.CreateAccessToken()
	if err != nil {
		return "", err
	}
	return token, nil
}

func (us *UserSubscription) Create() error {
	err := config.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "user_id"}, {Name: "author_id"}},
		DoUpdates: clause.AssignmentColumns([]string{"updated_at"}),
	}).Create(us).Error
	if err != nil {
		return err
	}
	return nil
}

func (us *UserSubscription) Delete() error {
	err := config.DB.Where("user_id = ? AND author_id = ?", us.UserID, us.AuthorID).Delete(us).Error
	if err != nil {
		return err
	}
	return nil
}
