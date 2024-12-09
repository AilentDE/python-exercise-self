package config

import (
	"fmt"
	"os"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

func InitDB() {
	var err error
	DB, err = gorm.Open(postgres.Open(os.Getenv("DB_URL")), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
		// DisableForeignKeyConstraintWhenMigrating: true,
	})
	if err != nil {
		panic(fmt.Sprintf("Failed to connect to database: %v", err))
	}

	// 設置連線池參數
	sqlDB, err := DB.DB()
	if err != nil {
		panic(fmt.Sprintf("Failed to configure database connection pool: %v", err))
	}

	// 設定最大開啟連線數
	sqlDB.SetMaxOpenConns(50) // 替換為適合你的值，通常應低於 PostgreSQL 的 `max_connections` 設置
	// 設定閒置連線數
	sqlDB.SetMaxIdleConns(10) // 設定保持閒置的連線數
	// 設定連線的最大生命週期
	sqlDB.SetConnMaxLifetime(30 * time.Minute) // 限制連線存活時間
	// 設定閒置連線的最大存活時間
	sqlDB.SetConnMaxIdleTime(5 * time.Minute) // 限制閒置連線存活時間

	// uuid4 extension
	err = DB.Exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";").Error
	if err != nil {
		panic(fmt.Sprintf("Failed to create extension: %v", err))
	}
}
