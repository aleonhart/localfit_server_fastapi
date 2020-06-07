DROP TABLE IF EXISTS activity_session;
DROP TABLE IF EXISTS activity_file;

CREATE TABLE activity_file (
	id INTEGER NOT NULL,
	filename VARCHAR NOT NULL,
	activity_type VARCHAR NOT NULL,
	is_manually_entered INTEGER DEFAULT 0,
	activity_collection VARCHAR,
	start_time_utc DATETIME NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (filename)
);

CREATE TABLE activity_session (
	id INTEGER NOT NULL,
	file_id INTEGER,
	start_time_utc DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(file_id) REFERENCES activity_file (id)
);