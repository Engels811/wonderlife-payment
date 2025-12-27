CREATE TABLE vat_rates (
    country_code CHAR(2) PRIMARY KEY,
    vat_rate DECIMAL(5,2) NOT NULL
);

INSERT INTO vat_rates VALUES
('DE', 19.00),
('AT', 20.00),
('NL', 21.00),
('FR', 20.00),
('IT', 22.00),
('ES', 21.00);
