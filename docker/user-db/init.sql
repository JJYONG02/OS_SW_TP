CREATE TABLE users (
    user_id  BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password)
VALUES  ('user1','1234'),
        ('user2','1234');