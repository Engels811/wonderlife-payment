CREATE OR REPLACE VIEW v_payments_clean AS
SELECT
    id,
    discord_id,
    provider,
    product,
    amount,
    status,
    created_at
FROM payments
WHERE status = 'paid';

CREATE OR REPLACE VIEW v_revenue_by_provider AS
SELECT
    provider,
    COUNT(*) AS payments,
    SUM(amount) AS revenue
FROM payments
WHERE status='paid'
GROUP BY provider;
