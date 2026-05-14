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

INSERT INTO posts (seller_id, title, description, price, status)
VALUES  (1, '맥북 에어 M5 팝니다', '새 상품급 상태입니다. user1입니다.', 1500000, 'SELLING'),
        (1, '아이패드 프로 13인치', '거의 안 쓴 제품입니다. user1입니다.', 1200000, 'IN_PROGRESS'),
        (2, '갤럭시 S24 울트라', '단순 개봉품입니다. user2 작성글입니다.', 1100000, 'SELLING');