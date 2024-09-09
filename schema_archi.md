```mermaid
graph TD;
    subgraph Front-end
        User[Utilisateur]
    end

    subgraph Back-end
        FlaskAPI[API Flask]
    end

    subgraph "Base de données"
        SQLite[SQLite Database]
    end

    subgraph Docker
        ElasticSearch[ElasticSearch]
    end

    User -->|HTTP Requests| FlaskAPI
    FlaskAPI -->|Search Queries| ElasticSearch
    FlaskAPI -->|Relational Data Queries| SQLite

```