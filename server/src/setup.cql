CREATE KEYSPACE app WITH REPLICATION = {'class' : 'SimpleStrategy','replication_factor' : 1};

CREATE TABLE app.users (
    id UUID,
    PRIMARY KEY (id)
);

CREATE TABLE app.files (
    id UUID,
    uid UUID,
    filename BLOB,
    iv BLOB,
    hash TEXT,
    date_added TIMESTAMP,
    PRIMARY KEY (uid, id)
);

-- INSERT INTO app.users (id) VALUES (79890d60-7f2d-4e50-a024-50b5ca17aaa1);

-- INSERT INTO app.files (id, uid, filename, iv, hash, date_added)
-- VALUES (92af4080-fe66-47e6-9989-b2f65f45a0bd, 79890d60-7f2d-4e50-a024-50b5ca17aaa1, 0x0000000000000003, 0x0000000000000003, 'f', '2011-02-03 04:05+0000');
