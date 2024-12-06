package db_method

import (
	"compare-with-robyn/config"
	"compare-with-robyn/models"
)

func CreateTables() {
	// [WARNNING] Doesn't know the reason that read history table would not be created sometimes
	// for _, m := range []interface{}{
	// 	&models.ReadHistory{},
	// 	&models.Message{},
	// 	&models.MessagePremission{},
	// 	&models.UserSubscription{},
	// 	&models.User{},
	// } {
	// 	config.DB.Migrator().DropTable(m)
	// 	config.DB.AutoMigrate(m)
	// }

	config.DB.Migrator().DropTable(&models.ReadHistory{})
	config.DB.Migrator().DropTable(&models.Message{})
	config.DB.Migrator().DropTable(&models.MessagePremission{})
	config.DB.Migrator().DropTable(&models.UserSubscription{})
	config.DB.Migrator().DropTable(&models.User{})

	config.DB.AutoMigrate(&models.ReadHistory{})
	config.DB.AutoMigrate(&models.Message{})
	config.DB.AutoMigrate(&models.MessagePremission{})
	config.DB.AutoMigrate(&models.UserSubscription{})
	config.DB.AutoMigrate(&models.User{})
}
