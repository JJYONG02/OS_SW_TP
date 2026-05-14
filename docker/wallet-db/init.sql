CREATE TABLE wallets (
    wallet_id BIGSERIAL PRIMARY KEY,
    user_id   BIGINT NOT NULL UNIQUE,
    balance   INT NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

INSERT INTO wallets (user_id, balance)
VALUES  (1, 1000000),
        (2, 1000000);