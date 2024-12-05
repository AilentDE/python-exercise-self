package db_method

import (
	"compare-with-robyn/config"
	"compare-with-robyn/models"
)

func CreateTables() {
	for _, m := range []interface{}{
		&models.ReadHistory{},
		&models.Message{},
		&models.MessagePremission{},
		&models.UserSubscription{},
		&models.User{},
	} {
		config.DB.Migrator().DropTable(m)
		config.DB.AutoMigrate(m)
	}
}
