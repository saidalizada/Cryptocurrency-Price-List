CREATE TABLE IF NOT EXISTS crypto_ranking_and_price (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    price_usd FLOAT,
    rank INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
