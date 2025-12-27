CREATE TABLE cancellations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT,
    cancelled_at DATETIME,
    cancelled_by VARCHAR(20)
);
