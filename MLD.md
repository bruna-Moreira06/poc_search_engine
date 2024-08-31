```mermaid
erDiagram
    user {
        INTEGER id PK
        TEXT username
        TEXT email
        TEXT password
        INTEGER role_id FK
    }
    roles {
        INTEGER id PK
        TEXT name
    }
    permissions {
        INTEGER id PK
        TEXT name
    }
    role_permissions {
        INTEGER role_id FK
        INTEGER permission_id FK
    }
    documents {
        INTEGER document_id PK
        TEXT name
        INTEGER uploaded_by FK
        TIMESTAMP upload_date
        BOOLEAN is_signed
    }
    labels {
        INTEGER id PK
        TEXT name
    }
    document_tags {
        INTEGER document_id FK
        INTEGER tag_id FK
    }
    
    user }o--|| roles : "role_id"
    role_permissions }o--|| roles : "role_id"
    role_permissions }o--|| permissions : "permission_id"
    documents }o--|| user : "uploaded_by"
    document_tags }o--|| documents : "document_id"
    document_tags }o--|| labels : "labels_id"

```

### Explication du diagramme

- **user** : Table pour gérer les utilisateurs, contenant l'identifiant de l'utilisateur, le nom d'utilisateur, l'email, le mot de passe et le rôle.
- **roles** : Table pour définir les rôles disponibles, associée aux utilisateurs et aux permissions.
- **permissions** : Table pour définir les différentes permissions.
- **role_permissions** : Table pour associer les rôles aux permissions (relation plusieurs-à-plusieurs).
- **documents** : Table pour gérer les documents, incluant les informations sur l'utilisateur qui a uploadé le document, la date d'upload, et si le document est signé.
- **labels** : Table pour gérer les étiquettes de documents.
- **document_tags** : Table pour associer les documents aux étiquettes (relation plusieurs-à-plusieurs).
