
DROP DATABASE game_analytics;
CREATE DATABASE game_analytics;
USE game_analytics;
CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20),
    gender VARCHAR(10),
    level VARCHAR(20),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
CREATE TABLE complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    country_code CHAR(3),
    timezone VARCHAR(100),
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
);
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    country_code CHAR(3),
    abbreviation VARCHAR(10)
);
CREATE TABLE competitor_rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    ranking INT,
    movement INT,
    points INT,
    competitions_played INT,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);
