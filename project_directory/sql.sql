CREATE DATABASE IF NOT EXISTS restaurant_reviews;
USE restaurant_reviews;


CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant VARCHAR(255) NOT NULL,
    reviewer VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    rating INT NOT NULL,
    review TEXT NOT NULL
);
