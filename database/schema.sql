-- Run on a new database. Existing installations: see README.md first.
CREATE DATABASE IF NOT EXISTS house_price_prediction CHARACTER SET utf8mb4;
USE house_price_prediction;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;
