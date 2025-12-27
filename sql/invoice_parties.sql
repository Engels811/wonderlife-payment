ALTER TABLE payments
ADD COLUMN customer_name VARCHAR(100),
ADD COLUMN customer_email VARCHAR(150),
ADD COLUMN customer_address TEXT,
ADD COLUMN company_name VARCHAR(150),
ADD COLUMN vat_id VARCHAR(50);
