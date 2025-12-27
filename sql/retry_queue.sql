CREATE TABLE payment_retries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT,
    provider VARCHAR(20),
    attempt INT DEFAULT 0,
    last_error TEXT,
    next_try DATETIME,
    active BOOLEAN DEFAULT TRUE
);
