CREATE TABLE wallets (
    wallet_id BIGSERIAL PRIMARY KEY,
    user_id   BIGINT NOT NULL UNIQUE,
    balance   INT NOT NULL DEFAULT 0 CHECK (balance >= 0)
);