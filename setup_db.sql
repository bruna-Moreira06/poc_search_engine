-- Table utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER,
    CONSTRAINT id_role_utilisateurs FOREIGN KEY (role_id) REFERENCES roles (role_id) on delete cascade
);

-- Table roles
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL,
    role_description TEXT NOT NULL
);

-- Table permissions
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT NOT NULL
);

-- Table permissions_des_roles
CREATE TABLE IF NOT EXISTS permissions_des_roles (
    role_id INTEGER,
    permission_id INTEGER,
    PRIMARY KEY (role_id, permission_id),
    CONSTRAINT id_role_permissions FOREIGN KEY (role_id) REFERENCES roles(role_id),
    CONSTRAINT id_permissions_permissions FOREIGN KEY (permission_id) REFERENCES permissions(permission_id)
);

-- Table documents
CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name TEXT NOT NULL,
    uploaded_by INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_signed BOOLEAN NOT NULL CHECK (is_signed IN (0, 1)),
    CONSTRAINT user_id_upload FOREIGN KEY (uploaded_by) REFERENCES utilisateurs(user_id)
);

-- Table etiquettes
CREATE TABLE IF NOT EXISTS etiquettes (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL
);

-- Table documentTags
CREATE TABLE IF NOT EXISTS documentTags (
    document_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (document_id, tag_id),
    CONSTRAINT document_id_docTag FOREIGN KEY (document_id) REFERENCES documents(document_id),
    CONSTRAINT tag_id_docTag FOREIGN KEY (tag_id) REFERENCES etiquettes(tag_id)
);

