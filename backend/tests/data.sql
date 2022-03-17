INSERT INTO users (username, email, password)
VALUES
  ('testtest', 'test@example.com', 'pbkdf2:sha256:260000$tCHFEP9NGOmj8A9J$88f3e9f3f6dfbefa6024149017f9db16141f3871e6c4e4bd9f284a7694f6f1bd'),
  ('otherother', 'other@example.com', 'pbkdf2:sha256:260000$tCHFEP9NGOmj8A9J$88f3e9f3f6dfbefa6024149017f9db16141f3871e6c4e4bd9f284a7694f6f1bd');

INSERT INTO posts (parent_id, author_id, content, created)
VALUES
  (NULL, 1, 'test', '2018-01-01 00:00:00');
