CREATE TABLE IF NOT EXISTS devices (
        device_id text PRIMARY KEY, 
        id text NOT NULL,
        displayName text NOT NULL,
        registration timestamp
);

CREATE TABLE IF NOT EXISTS users (
        user_id text PRIMARY KEY, 
        givenName text
);