CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS uploads (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	filename TEXT NOT NULL UNIQUE,
	filepath TEXT NOT NULL UNIQUE,
	userid INTEGER NOT NULL,
	FOREIGN KEY (userid) REFERENCES users(id)
);	
