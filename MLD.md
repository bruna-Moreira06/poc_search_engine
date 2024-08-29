```mermaid
erDiagram
    utilisateurs {
        INTEGER user_id PK
        TEXT username
        TEXT email
        TEXT password
        INTEGER role_id FK
    }
    roles {
        INTEGER role_id PK
        TEXT role_name
    }
    permissions {
        INTEGER permission_id PK
        TEXT permission_name
    }
    permissions_des_roles {
        INTEGER role_id FK
        INTEGER permission_id FK
    }
    documents {
        INTEGER document_id PK
        TEXT document_name
        INTEGER uploaded_by FK
        TIMESTAMP upload_date
        BOOLEAN is_signed
    }
    etiquettes {
        INTEGER tag_id PK
        TEXT tag_name
    }
    document_tags {
        INTEGER document_id FK
        INTEGER tag_id FK
    }
    
    utilisateurs }o--|| roles : "role_id"
    permissions_des_roles }o--|| roles : "role_id"
    permissions_des_roles }o--|| permissions : "permission_id"
    documents }o--|| utilisateurs : "uploaded_by"
    document_tags }o--|| documents : "document_id"
    document_tags }o--|| etiquettes : "tag_id"

```

### Explication du diagramme

- **utilisateurs** : Table pour gérer les utilisateurs, contenant l'identifiant de l'utilisateur, le nom d'utilisateur, l'email, le mot de passe et le rôle.
- **rôles** : Table pour définir les rôles disponibles, associée aux utilisateurs et aux permissions.
- **permissions** : Table pour définir les différentes permissions.
- **permissions_des_rôles** : Table pour associer les rôles aux permissions (relation plusieurs-à-plusieurs).
- **documents** : Table pour gérer les documents, incluant les informations sur l'utilisateur qui a uploadé le document, la date d'upload, et si le document est signé.
- **étiquettes** : Table pour gérer les étiquettes de documents.
- **documentTags** : Table pour associer les documents aux étiquettes (relation plusieurs-à-plusieurs).

Utiliser Mermaid pour créer des MLD est une excellente façon de documenter et visualiser la structure de ta base de données dans tes projets. N'hésite pas à poser d'autres questions ou demander plus de détails !
