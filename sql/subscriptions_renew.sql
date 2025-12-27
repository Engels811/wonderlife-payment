ALTER TABLE subscriptions
ADD COLUMN auto_renew BOOLEAN DEFAULT FALSE,
ADD COLUMN last_renewed DATETIME,
ADD COLUMN payment_provider VARCHAR(20),
ADD COLUMN price_cents INT,
ADD COLUMN billing_interval_days INT;
