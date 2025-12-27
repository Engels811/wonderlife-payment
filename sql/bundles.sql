CREATE TABLE product_bundles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bundle_name VARCHAR(100),
    role_id BIGINT
);

CREATE TABLE bundle_items (
    bundle_id INT,
    product_name VARCHAR(100)
);
