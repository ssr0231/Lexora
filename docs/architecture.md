# Lexora — System Architecture

**Version:** 0.1  
**Status:** Draft  
**Project:** Lexora

---

## 1. Architecture Overview

Lexora will use a modular web application architecture consisting of:

- React + TypeScript frontend
- FastAPI + Python backend
- PostgreSQL database
- pgvector for vector similarity search
- Supabase Authentication
- Supabase Storage for uploaded documents
- AI/LLM services for answer generation
- Background processing for document ingestion

High-level architecture:

User
  ↓
React Frontend
  ↓ HTTPS
FastAPI Backend
  │
  ├── Authentication & Authorization
  ├── Client Management
  ├── Document Management
  ├── Research
  └── AI/RAG Pipeline
  │
  ├── PostgreSQL + pgvector
  ├── Supabase Storage
  └── LLM Provider

---

## 2. Main Components

### 2.1 Frontend

The frontend will be built using React and TypeScript.

Responsibilities:

- User interface
- Authentication state
- Client selection
- Client profile display
- Research interface
- Conversation display
- Citation display
- Research history
- Loading and error states

The frontend will communicate with the backend through HTTP APIs.

---

### 2.2 Backend

The backend will be built using Python and FastAPI.

Responsibilities:

- API endpoints
- Business logic
- Authorization checks
- Client management
- Document management
- Research orchestration
- Retrieval pipeline
- AI integration
- Citation handling
- Research history
- Feedback

The backend will act as the main application layer between the frontend and data/AI services.

---

### 2.3 PostgreSQL Database

PostgreSQL will store structured application data such as:

- Users
- Clients
- User-client assignments
- Documents
- Document metadata
- Document chunks
- Research sessions
- Questions
- Answers
- Citations
- Feedback

The database will also use pgvector for storing and searching document embeddings.

---

### 2.4 Supabase Authentication

Supabase Auth will handle user authentication and session management.

Application-level authorization will determine what authenticated users are allowed to access.

Database-level policies will be considered for enforcing client data isolation.

---

### 2.5 Supabase Storage

Supabase Storage will store the original regulatory PDF files.

The database will store metadata and references to the stored files rather than storing the PDF contents directly in normal relational rows.

---

### 2.6 AI/RAG Pipeline

The AI system will use a Retrieval-Augmented Generation approach.

The retrieval process will:

1. Receive the user's question.
2. Convert the question into a searchable representation.
3. Retrieve relevant document chunks.
4. Apply appropriate filters such as document status and user/client access.
5. Provide relevant evidence to the language model.
6. Generate an answer based on the retrieved evidence.
7. Associate supporting citations with the answer.

The system should avoid relying solely on the language model's pretrained knowledge for regulatory answers.

---

### 2.7 Document Ingestion Pipeline

Uploaded regulatory documents will pass through a processing pipeline:

PDF
  ↓
Validation
  ↓
Text extraction
  ↓
OCR if required
  ↓
Text normalization
  ↓
Chunking
  ↓
Embedding generation
  ↓
PostgreSQL + pgvector

The original PDF will remain available through Supabase Storage.

Page information will be preserved where possible so that generated answers can reference the original document.

---

## 3. Main Research Flow

For a client-specific research question:

User
  ↓
Select Client
  ↓
Enter Question
  ↓
Frontend sends request
  ↓
FastAPI
  ↓
Authenticate User
  ↓
Authorize Client Access
  ↓
Load Relevant Client Context
  ↓
Retrieve Regulatory Evidence
  ↓
Build AI Context
  ↓
LLM
  ↓
Answer + Citations
  ↓
Save Research
  ↓
Return Response
  ↓
Frontend

The same flow can be used for general research without client-specific context.

---

## 4. Security Architecture

Security will be implemented across multiple layers.

### Authentication

Supabase Auth will verify the user's identity.

### Backend Authorization

FastAPI will verify whether the authenticated user is allowed to access requested resources.

### Database Authorization

PostgreSQL policies may be used to provide an additional layer of protection for sensitive client data.

### Retrieval Authorization

Client-specific documents and research must be filtered according to the user's permissions before being included in AI context.

### Secret Management

API keys and credentials will be stored using environment variables and will not be committed to Git.

---

## 5. Deployment Architecture

The initial deployment will use free or low-cost managed services.

Proposed deployment:

User
  ↓
Vercel
  ↓
React Frontend
  ↓ HTTPS
Render
  ↓
FastAPI Backend
  ↓
Supabase
  ├── PostgreSQL + pgvector
  ├── Authentication
  └── Storage

The architecture should remain simple enough for a portfolio project while allowing individual components to be replaced or expanded later.

---

## 6. Technology Decisions

| Component | Technology | Reason |
|---|---|---|
| Frontend | React + TypeScript | Modern component-based web development |
| Backend | FastAPI + Python | Strong fit for APIs and AI/document processing |
| Database | PostgreSQL | Relational data model and strong consistency |
| Vector Search | pgvector | Allows vector search within PostgreSQL |
| Authentication | Supabase Auth | Managed authentication integrated with our database stack |
| File Storage | Supabase Storage | Managed storage for uploaded documents |
| AI/RAG | Python | Strong ecosystem for AI and document processing |
| Frontend Hosting | Vercel | Simple deployment for React applications |
| Backend Hosting | Render | Simple deployment for FastAPI |
| Version Control | Git + GitHub | Source control and project collaboration |

---

## 7. Architectural Principles

The project will follow these principles:

1. Keep the MVP simple and avoid unnecessary infrastructure.
2. Separate frontend, backend, data, and AI responsibilities.
3. Keep business logic in the backend rather than the frontend.
4. Treat regulatory documents as source evidence rather than editable AI knowledge.
5. Preserve document and page information for citation traceability.
6. Enforce client data isolation at the backend and data layers.
7. Avoid exposing secrets in source code.
8. Keep AI components replaceable where practical.
9. Build for learning and maintainability rather than premature scale.


