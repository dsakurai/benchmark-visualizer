CREATE TABLE USERS
(
    USER_ID          BIGINT AUTO_INCREMENT PRIMARY KEY,
    USERNAME         VARCHAR(128),
    MAIL             VARCHAR(50) UNIQUE,
    PASSWORD         VARCHAR(128) NOT NULL
);

CREATE TABLE CONSTRUCTION_TREES
(
  TREE_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
  USER_ID BIGINT,
  TREE_DATA BLOB,
  CREATED_TIME TIMESTAMP
);
