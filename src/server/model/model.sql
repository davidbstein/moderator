
DROP TABLE users CASCADE;
CREATE TABLE IF NOT EXISTS users (
 u_email varchar(127),
 domain varchar(127),
 info JSON,
 PRIMARY KEY (u_email)
);
CREATE INDEX IF NOT EXISTS user_domains ON users (domain);

DROP TABLE orgs CASCADE;
CREATE TABLE IF NOT EXISTS orgs (
 domain varchar(128),
 moderators JSON,
 title JSON,
 PRIMARY KEY (domain)
);

DROP TABLE events CASCADE;
CREATE TABLE IF NOT EXISTS events (
 id BIGSERIAL NOT NULL PRIMARY KEY,
 domain varchar(127),
 owner_email varchar(127),
 lookup_id varchar(64),
 moderators JSON,
 title varchar(255),
 description JSON
);
CREATE INDEX IF NOT EXISTS event_lookup_id on events (lookup_id);
CREATE INDEX IF NOT EXISTS event_domain on events (domain);

DROP TABLE questions CASCADE;
CREATE TABLE IF NOT EXISTS questions (
 id BIGSERIAL NOT NULL PRIMARY KEY,
 e_id int,
 flagged boolean,
 flag_note JSON,
 content JSON,
 score int,
 comment_count int
);
CREATE INDEX IF NOT EXISTS questions_event_idx ON questions (e_id, id);

DROP TABLE comments CASCADE;
CREATE TABLE IF NOT EXISTS comments (
 id BIGSERIAL NOT NULL PRIMARY KEY,
 q_id int,
 owner_email varchar(127),
 content JSON,
 score int
);
CREATE INDEX IF NOT EXISTS comment_owner_emails ON comments (q_id, id);
CREATE INDEX IF NOT EXISTS comment_owner_emails ON comments (owner_email);

DROP TABLE question_votes CASCADE;
CREATE TABLE IF NOT EXISTS question_votes (
 q_id int NOT NULL,
 user_email varchar(127) NOT NULL,
 score int,
 PRIMARY KEY (q_id, user_email)
);

DROP TABLE comment_votes CASCADE;
CREATE TABLE IF NOT EXISTS comment_votes (
 c_id int NOT NULL,
 q_id int NOT NULL,
 user_email varchar(127),
 score int,
 PRIMARY KEY (c_id, user_email)
);
CREATE INDEX IF NOT EXISTS comment_votes_q_id ON comment_votes (q_id, c_id);
