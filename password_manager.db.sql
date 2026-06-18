BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_logs" (
	"id"	INTEGER,
	"username"	TEXT,
	"action"	TEXT,
	"ip_address"	TEXT,
	"timestamp"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"success"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT NOT NULL,
	"salt"	TEXT NOT NULL,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"last_login"	TIMESTAMP,
	"is_active"	INTEGER DEFAULT 1,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS "idx_logs_username" ON "auth_logs" (
	"username"
);
CREATE INDEX IF NOT EXISTS "idx_username" ON "users" (
	"username"
);
COMMIT;
