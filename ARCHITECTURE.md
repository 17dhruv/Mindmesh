MindMesh Architecture (End-to-End)

This document explains the complete system architecture of MindMesh, starting from the MVP and evolving naturally toward a full-scale, team-based, enterprise-ready platform.

The architecture is intentionally designed to:

Validate the core AI value early

Avoid premature complexity

Scale incrementally without rewrites

1️⃣ Architectural Principles

MindMesh is built on the following core principles:

AI-first, not infra-first
The AI planning logic is the core value; infrastructure supports it.

Human-in-the-loop by design
AI proposes plans, humans approve them.

Single source of truth
Business logic lives in the backend, not the frontend or AI.

Progressive complexity
Start simple, evolve only when real constraints appear.

2️⃣ High-Level System Overview (MVP)

At a high level, MindMesh consists of four layers:

User
 ↓
Frontend (Next.js)
 ↓
Backend (FastAPI)
 ↓
Database (PostgreSQL via Supabase)
 ↓
AI Services (OpenAI)


Each layer has strict responsibilities.

3️⃣ Frontend Architecture (Next.js)
Role of the Frontend

The frontend is a presentation and interaction layer only.

It is responsible for:

Collecting raw user thoughts

Displaying AI-generated plans

Rendering task lists and graphs

Allowing users to mark progress

Managing authentication state

It is not responsible for:

Planning logic

AI calls

Database writes

Business rules

Key Frontend Modules

Auth UI

Login / signup (Supabase Auth)

Thought Input (Chat UI)

Free-form text input

Plan Review UI

Displays AI-generated plan

Allows iteration/refinement

Graph Visualization

Node-based roadmap (React Flow)

Execution View

Simple grouped task list

The frontend communicates only with backend APIs.

4️⃣ Backend Architecture (FastAPI Monolith)
Why a Monolith First

MindMesh starts as a single FastAPI service to:

Reduce cognitive overhead

Enable rapid iteration

Keep state management simple

Avoid distributed-system complexity

This backend is the system’s brain.

Backend Responsibilities

Authentication validation

AI orchestration

Plan lifecycle management

Task and subtask logic

State enforcement (draft → accepted)

Graph data generation

Security and rate limiting

Backend Layering

Internally, the backend is structured into logical layers:

API Layer (Routes)
 ↓
Application Layer (Business Logic)
 ↓
AI Orchestration Layer
 ↓
Data Access Layer

Plan State Machine (Critical)

Every plan follows a strict lifecycle:

DRAFT → ACCEPTED → ARCHIVED


Rules:

AI can modify plans only in DRAFT

Once ACCEPTED, structure is immutable

Only task status updates are allowed

Replanning creates a new plan

This guarantees:

User trust

Predictable behavior

Clean history

5️⃣ AI Architecture (Planning Engine)

The AI is used only as a planner, never as an executor.

AI Interaction Flow

User submits raw thoughts

Backend sends input to AI

AI returns structured JSON:

Tasks

Groups

Subtasks

Priorities

Backend validates output against schema

User reviews and iterates

User explicitly accepts the plan

The AI never:

Writes directly to the database

Changes accepted plans

Acts without user confirmation

AI Design Constraints

Strict JSON schema enforcement

Cost limits per user

Cached outputs

No fine-tuning in MVP

Planning-only usage

6️⃣ Database Architecture (MVP)
PostgreSQL via Supabase

For the MVP, MindMesh uses a single relational database.

Core entities:

Users

Plans

Tasks

Subtasks

This keeps:

Data consistency high

Queries simple

Debugging easy

Why No Graph DB Initially

Although MindMesh uses graph visualization, the graph is derived, not stored.

Task relationships are stored relationally

Graph nodes and edges are generated in memory

Neo4j is introduced only if/when required

This avoids premature optimization.

7️⃣ Graph Architecture (MVP)

The graph is a visual representation, not a data store.

Graph Generation Flow

Backend fetches tasks + subtasks

Converts them into:

Nodes

Edges

Sends graph data to frontend

Frontend renders graph using React Flow

Graph updates:

Occur only after plan acceptance

Reflect task status changes

Do not change structure

8️⃣ Security Architecture
Authentication

Supabase Auth handles identity

JWT tokens passed to backend

Authorization

Backend validates user ownership

Supabase Row Level Security (RLS) as defense-in-depth

AI Security

API keys stored backend-only

Rate limiting enforced

Sensitive inputs minimized

9️⃣ Deployment Architecture (MVP)
Vercel
 (Next.js)
     ↓
Railway / Render
 (FastAPI)
     ↓
Supabase
 (PostgreSQL + Auth)
     ↓
OpenAI API


This setup:

Minimizes DevOps

Enables fast iteration

Is production-grade for MVP

🔄 Architecture Evolution Path

MindMesh is designed to evolve without rewrites.

Phase 2: Retention & Intelligence

Add vector database (Qdrant)

Add Redis for caching

Add background jobs

Keep monolith

Phase 3: Teams

Multi-tenant schema

Role-based permissions

Shared plans

Still one backend

Phase 4: Scale & Optimization

Introduce Neo4j (if needed)

Partial service separation

Read replicas

Phase 5: Enterprise

SSO

Audit logs

Compliance tooling

Optional DB migration to self-hosted Postgres

🔚 End-State Architecture (Vision)

At full scale, MindMesh becomes:

Clients (Web / Mobile)
   ↓
API Gateway
   ↓
Core Services (AI, Planning, Collaboration)
   ↓
Databases (Postgres + Graph + Vector)
   ↓
AI Providers (Pluggable)


But this is earned, not assumed.

🧭 Final Architectural Summary

Start simple

Protect the AI → clarity loop

Add complexity only when forced by real usage

Never sacrifice human control

Architecture should serve thinking, not impress diagrams

MindMesh’s architecture exists to turn thought into action — nothing more, nothing less.