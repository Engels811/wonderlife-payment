ALTER TABLE payments
ADD COLUMN invoice_number VARCHAR(50),
ADD COLUMN invoice_pdf VARCHAR(255);

CREATE INDEX idx_invoice_number ON payments(invoice_number);
