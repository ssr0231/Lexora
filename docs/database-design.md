# Lexora — Database Design

**Version:** 0.1  
**Status:** Draft  
**Project:** Lexora

---

## 1. Database Overview

Lexora will use PostgreSQL as its primary relational database.

The database will store application data such as:

- Users
- Clients
- User-client assignments
- Regulatory and client documents
- Document chunks
- Research sessions
- Conversation messages
- Citations
- Feedback

PostgreSQL will also use the `pgvector` extension to store and search document embeddings for the RAG pipeline.

---

## 2. Tables

### 2.1 Users

Stores application-level information about Lexora users.

| Column | Description |
|---|---|
| id | Unique user identifier |
| full_name | User's name |
| role | User's application role |
| created_at | Account creation timestamp |

Authentication credentials will be managed by Supabase Auth rather than stored directly in this table.

---

### 2.2 Clients

Stores information about businesses served by the CA firm.

| Column | Description |
|---|---|
| id | Unique client identifier |
| name | Client/business name |
| industry | Client industry |
| entity_type | Legal/business entity type |
| state | Primary state |
| gst_registered | Whether the client is GST registered |
| gstin | GST identification number |
| annual_turnover | Approximate annual turnover |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |

---

### 2.3 User Clients

Associates users with clients they are authorized to access.

This represents a many-to-many relationship between users and clients.

| Column | Description |
|---|---|
| id | Unique assignment identifier |
| user_id | Reference to user |
| client_id | Reference to client |
| assigned_at | Assignment timestamp |

Example:

```text
User A → Client X
User A → Client Y
User B → Client X