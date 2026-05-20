CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    brand_id INT,
    brand_name VARCHAR(100),
    loves_count INT,
    rating DECIMAL(4,3),
    reviews INT,
    price_usd DECIMAL(10,2),
    primary_category VARCHAR(100),
    secondary_category VARCHAR(100),
    tertiary_category VARCHAR(100),
    sephora_exclusive BOOLEAN
);

CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    author_id VARCHAR(100),
    rating DECIMAL(2,1),
    is_recommended BOOLEAN,
    helpfulness DECIMAL(5,2),
    submission_time DATETIME,
    review_text TEXT,
    review_title VARCHAR(255),
    skin_tone VARCHAR(100),
    eye_color VARCHAR(50),
    skin_type VARCHAR(100),
    hair_color VARCHAR(50),
    product_id VARCHAR(50),

    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);