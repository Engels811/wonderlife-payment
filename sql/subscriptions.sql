CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id BIGINT NOT NULL,
    product VARCHAR(100),
    role_id BIGINT,
    start_date DATETIME,
    end_date DATETIME,
    active BOOLEAN DEFAULT TRUE
);
