CREATE TYPE post_status AS ENUM ('SELLING', 'IN_PROGRESS', 'SOLD');

CREATE TABLE posts (
    post_id     BIGSERIAL PRIMARY KEY,
    seller_id   BIGINT NOT NULL,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    price       INT NOT NULL CHECK (price >= 0),
    status      post_status NOT NULL DEFAULT 'SELLING',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);