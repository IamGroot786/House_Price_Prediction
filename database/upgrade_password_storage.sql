-- Widen the legacy column without changing existing account values.
USE house_price_prediction;
ALTER TABLE users MODIFY password VARCHAR(255) NOT NULL;
