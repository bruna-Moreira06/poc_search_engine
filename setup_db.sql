-- Table utilisateurs
CREATE TABLE utilisateurs (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES rôles(role_id)
);

-- Table rôles
CREATE TABLE rôles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL
);

-- Table permissions
CREATE TABLE permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT NOT NULL
);

-- Table permissions_des_rôles
CREATE TABLE permissions_des_rôles (
    role_id INTEGER,
    permission_id INTEGER,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES rôles(role_id),
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id)
);

-- Table documents
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name TEXT NOT NULL,
    uploaded_by INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_signed BOOLEAN NOT NULL CHECK (is_signed IN (0, 1)),
    FOREIGN KEY (uploaded_by) REFERENCES utilisateurs(user_id)
);

-- Table étiquettes
CREATE TABLE étiquettes (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL
);

-- Table documentTags
CREATE TABLE documentTags (
    document_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (document_id, tag_id),
    FOREIGN KEY (document_id) REFERENCES documents(document_id),
    FOREIGN KEY (tag_id) REFERENCES étiquettes(tag_id)
);