DROP TABLE IF EXISTS interest_points;


CREATE TABLE abbreviation (
	abbrev_id INTEGER NOT NULL,
	abbrev VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (abbreviation)
);


CREATE TABLE interest_point (
	interest_point_id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
    location_name VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    gps_lat DECIMAL NOT NULL,
    gps_long DECIMAL NOT NULL,
	FOREIGN KEY(abbrev) REFERENCES abbreviation (abbrev)
	PRIMARY KEY (interest_point_id),
);
