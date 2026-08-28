# TransformIQ — Business Transformation AI (AI Solution Builder)

> **From Business Chaos to Implementation-Ready Solutions.**  
> *AI Business Consultant + Business Analyst + Solution Architect + Product Strategist in One Unified Enterprise Platform.*  
> **Chaos2Commit Hackathon 2026**

---

## 1. Executive Summary & Product Vision

TransformIQ is an enterprise-grade digital transformation platform designed to convert unstructured business ideas, challenges, prompts, and enterprise documents (SOPs, BRDs, PDFs, Word, PPTX) into **verifiable, implementation-ready solution blueprints**.

Unlike traditional AI documentation tools, TransformIQ provides an **end-to-end transformation operating system**:

```text
BUSINESS CHAOS
       ↓
DOCUMENT / PROMPT INGESTION (PDF, Word, PPTX, TXT)
       ↓
BUSINESS CONTEXT & RAG ENGINE
       ↓
AI DISCOVERY COMPANION (Multilingual: EN, HI, GU)
       ↓
CURRENT-STATE (AS-IS) & BUSINESS ANALYSIS
       ↓
8-DIMENSION GAP ANALYSIS (Process, Tech, AI, Data, People, Security, Automation, Integration)
       ↓
AI & AUTOMATION RECOMMENDATION ENGINE ("Why this recommendation?" Explainable AI)
       ↓
INTERACTIVE REACT FLOW SOLUTION ARCHITECTURE (HLD & LLD)
       ↓
PROCESS INTELLIGENCE DESIGNER (BPMN Workflow with Swimlanes & Cycle Time Analytics)
       ↓
DATABASE & INTEGRATION DESIGNER (PostgreSQL ER Schema & SQL DDL)
       ↓
REST API CATALOG (OpenAPI 3.0 Specifications)
       ↓
AI UX DESIGNER & INTERACTIVE WIREFRAME MOCKUPS
       ↓
TRANSFORMATION ROADMAP & STAFFING COST ESTIMATION
       ↓
DYNAMIC WHAT-IF SIMULATOR (Automation %, Team Size, Budget, Timeline & Instant ROI)
       ↓
TRANSFORMIQ READINESS SCORECARD (6 Dimensions)
       ↓
HUMAN-IN-THE-LOOP GOVERNANCE & APPROVAL WORKFLOW
       ↓
MASTER IMPLEMENTATION BLUEPRINT (24 Enterprise Dimensions)
       ↓
REAL FILE EXPORTS (PDF via ReportLab, Word DOCX, Excel XLSX, PowerPoint PPTX)
```

---

## 2. Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript & Vite
- **Styling**: Tailwind CSS, Lucide Icons, Glassmorphic Enterprise UI
- **Diagrams**: React Flow for interactive Architecture & BPMN workflows
- **Charts**: Recharts (Radar maturity scorecards, latency comparisons)
- **Routing & State**: React Router v6, TanStack Query, Axios
- **Multilingual Support**: Built-in i18n for **English**, **Hindi (हिन्दी)**, and **Gujarati (ગુજરાતી)**

### Backend
- **Framework**: FastAPI (Python 3.10+) with Pydantic v2 validation
- **ORM & Database**: SQLAlchemy 2.0 Async (SQLite zero-config by default / PostgreSQL with pgvector)
- **Security & Multi-Tenancy**: JWT Bearer authentication, PBKDF2/Bcrypt password hashing, Role-Based Access Control (`ADMIN`, `OWNER`, `MANAGER`, `ANALYST`, `ARCHITECT`, `MEMBER`, `VIEWER`), Organization/Workspace data isolation
- **Document Extractors**: `pypdf`, `python-docx`, `python-pptx` with automated chunking and keyword/semantic RAG
- **AI Orchestrator**: Modular multi-agent engine supporting Azure OpenAI GPT-4o, OpenAI GPT-4o, and Contextual Smart Generation for zero-credential offline evaluation
- **Real File Exporters**:
  - **PDF**: `ReportLab` executive blueprint generation with styled tables and cover pages
  - **Word**: `python-docx` enterprise spec documentation
  - **Excel**: `openpyxl` multi-sheet workbooks (Requirements, Gaps, Staffing Budget, API Catalog)
  - **PowerPoint**: `python-pptx` presentation slides

---

## 3. Flagship Demo Scenario: Customer Support Transformation

TransformIQ comes pre-seeded with a flagship enterprise scenario ready for immediate evaluation:

- **Enterprise**: Apex Global Retail & Logistics
- **Business Chaos**: E-commerce company receives 45,000+ complaints monthly. Manual email reading causes a 48-hour triage backlog, 18% department misrouting rate, and $420k in wasted administrative labor.
- **AI Transformation Output**:
  1. Multi-channel automated ingestion (REST + Webhook)
  2. Sub-second NLP intent classification and sentiment scoring
  3. SOP knowledge grounding via semantic RAG
  4. Human-in-the-Loop exception queue for cases with confidence < 85%
  5. 87.5% cycle time reduction (48 Hours → 12 Minutes)
  6. 340% 12-Month Net ROI ($138,500 budget investment)

---

## 4. Quick Start & Local Execution

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt email-validator
# Run backend on port 8000
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*The database and pre-seeded demo scenarios initialize automatically on startup.*
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
- Frontend Web Application: [http://localhost:5173](http://localhost:5173)

---

## 5. Role-Based Access Control (RBAC) & Evaluation Test Accounts

TransformIQ features strict enterprise authorization across 7 specialized transformation roles. For immediate hackathon judging & evaluation:

| Role | Email | Password | Primary Scope & Access |
| :--- | :--- | :--- | :--- |
| **ADMIN** | `admin@transformiq.local` | `TransformIQ@2026` | Platform administration, users, workspaces, AI usage telemetry, and immutable audit logs. |
| **PROJECT OWNER** | `owner@transformiq.local` | `TransformIQ@2026` | Full transformation initiative ownership: discovery, requirements, architecture, and team assignment. |
| **BUSINESS ANALYST** | `analyst@transformiq.local` | `TransformIQ@2026` | Operational problem analysis, stakeholder matrices, functional requirements, and 8-dimension gap matrix. |
| **SOLUTION ARCHITECT** | `architect@transformiq.local` | `TransformIQ@2026` | Reactive HLD architecture, BPMN workflows, PostgreSQL schemas, and OpenAPI contracts. |
| **MANAGER** | `manager@transformiq.local` | `TransformIQ@2026` | Transformation score analysis, projected ROI evaluation, risk management, and final blueprint approvals. |
| **MEMBER** | `member@transformiq.local` | `TransformIQ@2026` | Workflow execution, discussions, assigned tasks, and document reviews. |
| **VIEWER** | `viewer@transformiq.local` | `TransformIQ@2026` | Read-only access to approved blueprints, architecture diagrams, and maturity metrics. |

> **Interactive Role Switcher**: When logged into the application, click the **"ROLE: ..."** pill in the top header bar to switch between all 7 roles in 1 click!

---

## 6. Docker Deployment

Launch the complete multi-container stack (Frontend, Backend, PostgreSQL with pgvector) via Docker Compose:

```bash
docker-compose up --build
```
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `localhost:5432`

---

## 7. Automated RBAC & Security Testing

Execute the comprehensive Pytest suite validating all 14 security rules, permission boundaries, and tenant isolation:

```bash
cd backend
pytest tests/test_rbac.py -v
```

Run the full automated test suite:

```bash
# Backend unit and integration tests
$env:PYTHONPATH="backend"
python -m pytest backend/tests

# Frontend production build verification
cd frontend
npm run build
```

---

## 8. Chaos2Commit Compliance Checklist

| Requirement | Implementation in TransformIQ | Status |
| :--- | :--- | :---: |
| **Real Frontend & Backend** | React 18 + Vite + TypeScript & FastAPI with REST endpoints | ✅ Complete |
| **Document Ingestion (PDF, DOCX, PPTX)** | `pypdf`, `python-docx`, `python-pptx` with contextual chunking & RAG | ✅ Complete |
| **8-Dimension Gap Analysis** | Process, Tech, AI, Data, People, Security, Automation, Integration | ✅ Complete |
| **Explainable AI ("Why?")** | Dedicated explainability modal on every recommendation with citations | ✅ Complete |
| **Interactive Architecture** | React Flow canvas with custom nodes, connections, and layout save | ✅ Complete |
| **BPMN Process Intelligence** | React Flow workflow with swimlanes, cycle times, and decision trees | ✅ Complete |
| **Database & API Designer** | PostgreSQL ER tables, SQL DDL generation, and OpenAPI 3.0 spec | ✅ Complete |
| **AI UX & Wireframes** | Personas, user journeys, and rendered interactive UI mockups | ✅ Complete |
| **What-If Simulation** | Live recalculation of ROI, cost, effort, timeline, and risk level | ✅ Complete |
| **Transformation Score** | Proprietary 6-dimension benchmark with radar chart visualization | ✅ Complete |
| **Human-in-the-Loop** | Approval workflow (`DRAFT`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`) | ✅ Complete |
| **Real Multi-Format Exports** | Real PDF (ReportLab), Word (DOCX), Excel (XLSX), PowerPoint (PPTX) | ✅ Complete |
| **Multilingual Support** | English, Hindi (हिन्दी), and Gujarati (ગુજરાતી) UI localization | ✅ Complete |
| **Centralized Administration** | Multi-tenant governance, AI token tracking, and immutable audit logs | ✅ Complete |
