CREATE TABLE IF NOT EXISTS USERS (
  user_id     BIGSERIAL PRIMARY KEY,
  email       VARCHAR(50) UNIQUE,
  password    VARCHAR(500),
  first_name  VARCHAR(200),
  last_name   VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS shirts (
  shirt_id      BIGSERIAL PRIMARY KEY,
  user_id       BIGINT NOT NULL REFERENCES users(user_id),
  name          VARCHAR(100),
  created       DATE,
  updated       DATE,
  text_content  VARCHAR(500),
  redirect_url  VARCHAR(500),
  qr_id         VARCHAR(100),
  image_id      VARCHAR(100),
  status        VARCHAR(50)
);
