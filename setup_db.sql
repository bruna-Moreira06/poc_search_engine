-- Table utilisateurs
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER,
    CONSTRAINT id_role_utilisateurs FOREIGN KEY (role_id) REFERENCES roles (id)
);

-- Table roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_roles TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Table permissions
CREATE TABLE IF NOT EXISTS permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_permissions TEXT NOT NULL
);

-- Table permissions_des_roles
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER,
    permission_id INTEGER,
    PRIMARY KEY (role_id, permission_id),
    CONSTRAINT id_role_permissions FOREIGN KEY (role_id) REFERENCES roles(id) on delete cascade, 
    CONSTRAINT id_permissions_permissions FOREIGN KEY (permission_id) REFERENCES permission(id) on delete cascade
);

-- Table documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_doc TEXT NOT NULL,
    uploaded_by INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_signed BOOLEAN NOT NULL CHECK (is_signed IN (0, 1)),
    CONSTRAINT user_id_upload FOREIGN KEY (uploaded_by) REFERENCES user(id)
);

-- Table etiquettes
CREATE TABLE IF NOT EXISTS labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_labels TEXT NOT NULL
);

-- Table documentTags
CREATE TABLE IF NOT EXISTS document_tags (
    document_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (document_id, tag_id),
    CONSTRAINT document_id_docTag FOREIGN KEY (document_id) REFERENCES documents(id) on delete cascade,
    CONSTRAINT tag_id_docTag FOREIGN KEY (tag_id) REFERENCES labels(id) on delete cascade
);
