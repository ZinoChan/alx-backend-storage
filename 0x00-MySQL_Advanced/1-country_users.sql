
-- create user table
-- attr: id, email, name, country

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country VARCHAR(2) NOT NULL DEFAULT 'US',
	CHECK (country IN ('US , CO , TN'))
)
