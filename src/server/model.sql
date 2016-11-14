
CREATE TABLE IF NOT EXISTS users (
 u_email varchar(127),
 domain varchar(127),
 info JSON,
 PRIMARY KEY (u_email)
);
CREATE INDEX IF NOT EXISTS user_domains ON users (domain);

CREATE TABLE IF NOT EXISTS orgs (
 domain varchar(128),
 moderators JSON,
 title JSON,
 PRIMARY KEY (domain)
);

CREATE TABLE IF NOT EXISTS events (
 e_id BIGSERIAL NOT NULL PRIMARY KEY,
 domain varchar(127),
 owner_email varchar(127),
 lookup_id varchar(64),
 moderators JSON,
 title varchar(255),
 description JSON
);
CREATE INDEX IF NOT EXISTS event_lookup_id on events (lookup_id);
CREATE INDEX IF NOT EXISTS event_domain on events (domain);

CREATE TABLE IF NOT EXISTS questions (
 q_id BIGSERIAL NOT NULL,
 e_id int,
 flagged boolean,
 flag_note JSON,
 content JSON,
 score int,
 comment_count int,
 PRIMARY KEY (e_id, q_id)
);

CREATE TABLE IF NOT EXISTS comments (
 c_id BIGSERIAL NOT NULL,
 q_id int,
 owner_email varchar(127),
 content JSON,
 score int,
 PRIMARY KEY (q_id, c_id)
);
CREATE INDEX IF NOT EXISTS comment_owner_emails ON comments (owner_email);

CREATE TABLE IF NOT EXISTS question_likes (
 q_id int,
 owner_email varchar(127),
 score int,
 PRIMARY KEY (q_id, owner_email)
);

CREATE TABLE IF NOT EXISTS comment_likes (
 c_id int,
 owner_email varchar(127),
 score int,
 PRIMARY KEY (c_id, owner_email)
);