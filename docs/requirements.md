# Lexora — Software Requirements Specification

**Version:** 0.1  
**Status:** Draft  
**Project:** Lexora  
**Client Scenario:** Sharma & Associates  
**Domain:** GST Regulatory Research  

---

## 1. Project Overview

Lexora is an AI-powered regulatory research assistant designed for CA professionals.

It helps compliance employees research GST-related questions by searching relevant regulatory documents, considering authorized client information, and generating evidence-backed answers with citations.

Lexora is intended to assist professional research. It does not replace professional judgment or provide autonomous tax or legal decisions.

---

## 2. Business Problem

Sharma & Associates is a fictional Delhi-based CA and tax-compliance firm serving approximately 300 small and medium-sized businesses.

Employees regularly research GST questions using Acts, Rules, notifications, circulars, and other regulatory documents.

The current process is largely manual:

Client question  
↓  
Search documents  
↓  
Read relevant sections  
↓  
Compare regulations  
↓  
Check client information  
↓  
Senior CA review

A typical question may take 30–60 minutes to research.

The main difficulty is not simply finding documents, but determining which information is relevant to a particular client's circumstances and verifying the conclusion against authoritative sources.

Lexora aims to make this research process faster, more consistent, and easier to verify.

---

## 3. Objectives

Lexora aims to:

1. Reduce the time spent on common GST research questions.
2. Help users find information relevant to a specific client.
3. Provide answers supported by source documents and citations.
4. Clearly communicate uncertainty or missing information.
5. Maintain appropriate access controls for confidential client data.
6. Provide a foundation for evaluating and improving AI-assisted research.

---

## 4. Users & Roles

### 4.1 Compliance Executive

The primary user who can:

- View assigned clients.
- Ask general and client-specific questions.
- Review AI answers and citations.
- Continue research through follow-up questions.
- View permitted research history.

### 4.2 Senior CA

Can perform the above activities and additionally:

- Review research performed by employees.
- Review supporting evidence.
- Provide feedback.
- Manage selected regulatory documents.

### 4.3 Administrator

Can:

- Manage users and roles.
- Assign users to clients.
- Manage client records.
- Manage the regulatory document library.
- Review basic system activity.

---

## 5. Functional Requirements

### 5.1 Authentication & Access

Lexora shall:

- Require users to authenticate before accessing protected functionality.
- Support the three defined user roles.
- Restrict functionality according to user permissions.
- Restrict users to their authorized clients and data.
- Allow administrators to deactivate users.

### 5.2 Client Management

Lexora shall allow authorized users to:

- Create and view client profiles.
- Store relevant information such as industry, entity type, state, GST status, GSTIN, and turnover.
- Assign users to clients.
- Update client information.
- Use authorized client information during client-specific research.

### 5.3 Document Management

Lexora shall:

- Allow authorized users to upload regulatory PDFs.
- Initially support GST Acts, GST Rules, CBIC Notifications, and CBIC Circulars.
- Store relevant document metadata such as title, type, dates, source, and status.
- Extract text from documents while preserving page information where possible.
- Support scanned PDFs through OCR where required.
- Track document processing status.
- Maintain basic document version and status information.
- Restrict document access according to permissions.

### 5.4 AI Regulatory Research

Lexora shall allow users to:

- Ask natural-language regulatory questions.
- Perform general research without selecting a client.
- Perform client-specific research using authorized client information.
- Retrieve relevant information from one or more regulatory documents.
- Generate answers based on retrieved evidence.
- Provide citations to supporting documents and pages where available.
- Explain the reasoning behind an answer in a concise manner.
- Identify missing information when it prevents reliable analysis.
- Indicate when sufficient evidence cannot be found.
- Ask follow-up questions within the same research session.

Lexora shall not present unsupported AI-generated information as verified regulatory advice.

### 5.5 Research History & Feedback

Lexora shall:

- Store research sessions for authorized users.
- Allow users to revisit permitted research.
- Maintain conversation context for follow-up questions.
- Allow users to mark answers as helpful or not helpful.
- Associate feedback with the relevant research question and answer.

Research involving client information must follow the same access restrictions as the associated client.

---

## 6. Non-Functional Requirements

### 6.1 Security

- Authentication and authorization must use secure, industry-standard mechanisms.
- Client data must be isolated between authorized users.
- Backend and database-level access controls must enforce permissions.
- Secrets and API keys must not be committed to Git.
- Production communication must use HTTPS.
- Sensitive information should not be unnecessarily exposed through logs or API responses.

### 6.2 Performance

- Normal UI interactions should remain responsive.
- Research requests should complete within a reasonable interactive time.
- Long-running document processing should run asynchronously.
- The system should handle documents containing hundreds of pages.

### 6.3 Reliability

- Processing and AI failures should be handled gracefully.
- Failed document processing should be identifiable and retryable where possible.
- Lack of evidence should never result in an answer being presented as verified.
- Document, page, chunk, and citation relationships must remain consistent.

### 6.4 Maintainability

- Frontend, backend, database, and AI/retrieval responsibilities should be clearly separated.
- Configuration and secrets should be externalized.
- Important architecture and setup decisions should be documented.
- Critical functionality should have automated tests.
- Git should be used for version control.

### 6.5 Observability

- Important application events and errors should be logged.
- AI and retrieval processing should expose enough non-sensitive information for debugging and evaluation.

---

## 7. MVP Scope

### 7.1 MVP Goal

The goal of the Lexora MVP is to demonstrate that CA professionals can use an AI-assisted regulatory research workflow to find relevant GST information faster and verify AI-generated answers against authoritative source documents.

### 7.2 In Scope

The MVP will include:

- User authentication.
- Basic roles and permissions.
- Client profiles.
- Client assignment.
- Regulatory PDF upload.
- GST regulatory documents.
- Document text extraction and processing.
- General regulatory research.
- Client-specific regulatory research.
- Retrieval of relevant regulatory information.
- AI-generated responses based on retrieved evidence.
- Source citations.
- Handling of insufficient evidence.
- Follow-up questions.
- Research history.
- Basic answer feedback.
- Basic security and audit controls.
- Deployment of the web application.

### 7.3 Out of Scope

The MVP will not include:

- GST return filing.
- Government-system integration.
- WhatsApp or email integrations.
- Mobile applications.
- Complete coverage of all Indian tax domains.
- Automatic client impact analysis.
- Automated regulatory alerts.
- Autonomous tax or legal decision-making.
- Complex enterprise SSO.
- Advanced analytics.
- Multi-agent autonomous workflows.
- Microservices or Kubernetes infrastructure.

---

## 8. Success Criteria

The MVP will be considered successful if:

- A user can securely log in.
- An authorized user can view and manage a client.
- A regulatory PDF can be uploaded and processed.
- Relevant information can be retrieved from the document.
- Users can ask general and client-specific questions.
- Answers are grounded in retrieved evidence.
- Answers contain traceable citations.
- The system can identify insufficient evidence.
- Unauthorized users cannot access another client's information.
- The complete workflow works on the deployed application.

We will later create a small evaluation dataset to measure:

- Retrieval quality.
- Citation correctness.
- Answer quality.
- Response time.

---

## 9. Future Scope

Potential future capabilities include:

- Regulatory change monitoring.
- Identifying potentially affected clients when a new regulation appears.
- Support for additional tax and regulatory domains.
- Advanced analytics.
- Email or WhatsApp integrations.
- Improved AI evaluation.
- More sophisticated document relationship and version analysis.

These capabilities are not part of the MVP.

---

## 10. Assumptions & Constraints

- Lexora is a portfolio and learning project based on a hypothetical CA client scenario.
- The initial regulatory scope is limited to GST.
- We will primarily use publicly available regulatory documents for demonstration.
- Development and deployment will prioritize free or low-cost services.
- AI providers and infrastructure may have usage or rate limitations.
- Lexora is a research-assistance tool and its output should be professionally verified.