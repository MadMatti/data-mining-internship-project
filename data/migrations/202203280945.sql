CREATE TABLE IF NOT EXISTS logs (
        id text PRIMARY KEY, 
        createDateTime timestamp NOT NULL,
        user_id text NOT NULL,
        userDisplayName text,
        device_id text,
        deviceDisplayName text
);