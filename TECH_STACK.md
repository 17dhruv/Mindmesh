# Mindmesh Technical Stack Documentation

## Overview

This document outlines the complete technical architecture for Mindmesh, from MVP to enterprise scale. The stack is designed for cost efficiency, developer productivity, and scalable growth.

## Core Technology Choices

### Frontend Foundation
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod
- **HTTP Client**: TanStack Query (React Query)
- **Graph Visualization**: React Flow
- **Icons**: Lucide React
- **Date Handling**: date-fns

### Backend Foundation
- **Framework**: FastAPI (Python 3.11+)
- **Database ORM**: SQLAlchemy 2.0 + Alembic
- **Validation**: Pydantic v2
- **Authentication**: Supabase Auth + custom middleware
- **Background Jobs**: Celery + Redis
- **AI Integration**: LiteLLM (unified AI API)
- **Rate Limiting**: slowapi
- **File Processing**: python-multipart

### Database & Storage
- **Primary Database**: Supabase (PostgreSQL 15+)
- **Authentication**: Supabase Auth
- **Real-time**: Supabase Realtime
- **File Storage**: Supabase Storage
- **Search**: PostgreSQL Full-Text → Typesense
- **Cache**: Redis (upstash for edge, self-hosted for scale)

### Infrastructure & Hosting
- **Frontend**: Vercel (Pro → Enterprise)
- **Backend**: Railway/Render (Multi-region)
- **Database**: Supabase (Pro → Enterprise)
- **CDN**: Vercel Edge Network
- **Monitoring**: Sentry + Vercel Analytics
- **Error Tracking**: Sentry
- **APM**: New Relic (Phase 3+)

---

## Phase-Based Implementation

### Phase 1: MVP Stack (Months 0-6)
**Target Cost**: ~$150/month

#### Frontend Dependencies
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",

    // Core Framework
    "@supabase/supabase-js": "^2.38.0",
    "@supabase/auth-helpers-nextjs": "^0.8.0",

    // State Management
    "zustand": "^4.4.0",

    // UI & Styling
    "tailwindcss": "^3.3.0",
    "@tailwindcss/typography": "^0.5.0",
    "@tailwindcss/forms": "^0.5.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",

    // UI Components (shadcn/ui)
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-separator": "^1.0.3",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-toast": "^1.1.5",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",

    // Forms & Validation
    "react-hook-form": "^7.47.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0",

    // Data Fetching
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",

    // Graph Visualization
    "reactflow": "^11.10.0",

    // Utilities
    "lucide-react": "^0.292.0",
    "date-fns": "^2.30.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0",
    "prettier": "^3.0.0",
    "prettier-plugin-tailwindcss": "^0.5.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  }
}
```

#### Backend Dependencies
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
asyncpg==0.29.0
supabase==1.0.4

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI Integration
litellm==1.1.1
openai==1.3.8
anthropic==0.7.7

# Background Jobs
celery==5.3.4
redis==5.0.1

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
slowapi==0.1.9

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
isort==5.12.0
mypy==1.7.1
```

#### Infrastructure Configuration
```yaml
# docker-compose.yml (Local Development)
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - REDIS_URL=redis://redis:6379

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

### Phase 2: Teams Stack (Months 6-18)
**Target Cost**: ~$800/month

#### Additional Frontend Dependencies
```json
{
  "dependencies": {
    // Real-time
    "@supabase/realtime-js": "^2.8.0",
    "pusher-js": "^8.0.0",

    // Advanced UI
    "@dnd-kit/sortable": "^8.0.0",
    "@dnd-kit/core": "^6.1.0",
    "recharts": "^2.8.0",
    "react-beautiful-dnd": "^13.1.1",

    // Date & Time
    "react-day-picker": "^8.9.0",
    "date-picker": "^0.1.0",

    // File Handling
    "react-dropzone": "^14.2.3",
    "file-saver": "^2.0.5",
    "react-pdf": "^7.5.1",

    // Rich Text
    "@tiptap/react": "^2.1.0",
    "@tiptap/starter-kit": "^2.1.0",

    // Forms Advanced
    "react-hook-form": "^7.48.0",
    "@hookform/resolvers": "^3.3.0",

    // Notifications
    "react-hot-toast": "^2.4.1",
    "web-push": "^3.6.0"
  }
}
```

#### Additional Backend Dependencies
```python
# Additional requirements for Phase 2
celery[redis]==5.3.4
flower==2.0.1  # Celery monitoring

# Search
typesense==0.11.0
postgresql-search==0.5.0

# Real-time
websockets==12.0
pusher==3.3.2

# Email & Notifications
resend==0.1.0
emails==0.6

# File Processing
pillow==10.1.0
python-magic==0.4.27

# Advanced Security
python-bcrypt==4.1.0
cryptography==41.0.8

# Scheduling
apscheduler==3.10.4

# Analytics
mixpanel==4.10.0
segment-analytics-python==4.3.0
```

#### Enhanced Infrastructure
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_PUSHER_KEY=${PUSHER_KEY}
      - NEXT_PUBLIC_TYPESENSE_KEY=${TYPESENSE_KEY}

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - PUSHER_APP_ID=${PUSHER_APP_ID}
      - TYPESENSE_HOST=${TYPESENSE_HOST}
    deploy:
      replicas: 2

  celery-worker:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      replicas: 3

  celery-beat:
    build: ./backend
    command: celery -A app.celery beat --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}

  flower:
    build: ./backend
    command: celery -A app.celery flower
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=${REDIS_URL}

  typesense:
    image: typesense/typesense:0.25.0
    environment:
      - TYPESENSE_API_KEY=${TYPESENSE_API_KEY}
    volumes:
      - typesense_data:/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  redis_data:
  typesense_data:
```

### Phase 3: Enterprise Stack (Months 18-36)
**Target Cost**: $5000+/month

#### Enterprise Frontend Dependencies
```json
{
  "dependencies": {
    // Authentication
    "@auth0/auth0-react": "^2.2.0",
    "@auth0/auth0-spa-js": "^2.1.0",

    // Advanced Analytics
    "recharts": "^2.8.0",
    "d3": "^7.8.5",
    "@types/d3": "^7.4.3",

    // Code Editing
    "monaco-editor": "^0.44.0",
    "@monaco-editor/react": "^4.6.0",

    // Advanced Tables
    "@tanstack/react-table": "^8.10.0",
    "react-table": "^7.8.0",

    // PDF & Export
    "react-pdf": "^7.5.1",
    "jspdf": "^2.5.1",
    "html2canvas": "^1.4.1",

    // Accessibility
    "@axe-core/react": "^4.8.0",

    // Performance
    "@next/bundle-analyzer": "^14.0.0",
    "web-vitals": "^3.5.0",

    // Security
    "dompurify": "^3.0.5",
    "helmet": "^7.1.0"
  }
}
```

#### Enterprise Backend Dependencies
```python
# Enterprise requirements
newrelic==9.2.0
sentry-sdk[fastapi]==1.38.0

# Advanced Security
auth0-python==4.0.0
cryptography==41.0.8
pyotp==2.9.0
qrcode[pil]==7.4.2

# Advanced Analytics
pandas==2.1.3
numpy==1.25.2
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0

# Advanced Database
psycopg2-binary==2.9.9
pgvector==0.2.3

# Enterprise Integrations
azure-identity==1.15.0
azure-keyvault-secrets==4.7.0
boto3==1.34.0

# Compliance & Audit
audit-log==0.2.1
compliance-checker==5.0.0

# Advanced Background Jobs
celery[redis]==5.3.4
celery-redbeat==2.0.0

# Advanced File Processing
pillow==10.1.0
opencv-python==4.8.1.78
python-docx==1.1.0

# API Gateway
fastapi-gateway==0.1.0
kombu==5.3.4
```

#### Enterprise Infrastructure
```yaml
# docker-compose.enterprise.yml
version: '3.8'
services:
  # API Gateway
  api-gateway:
    build: ./gateway
    ports:
      - "80:80"
      - "443:443"
    environment:
      - BACKEND_URLS=${BACKEND_URLS}
      - RATE_LIMITS=${RATE_LIMITS}
    volumes:
      - ./ssl:/etc/ssl/certs

  # Frontend (Multiple regions)
  frontend-us:
    build: ./frontend
    environment:
      - REGION=us
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.labels.region == us

  frontend-eu:
    build: ./frontend
    environment:
      - REGION=eu
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.labels.region == eu

  # Backend Services
  ai-service:
    build: ./services/ai
    environment:
      - DATABASE_URL=${AI_DATABASE_URL}
      - REDIS_CLUSTER=${REDIS_CLUSTER}
    deploy:
      replicas: 5
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

  task-service:
    build: ./services/tasks
    environment:
      - DATABASE_URL=${TASK_DATABASE_URL}
      - REDIS_CLUSTER=${REDIS_CLUSTER}
    deploy:
      replicas: 3

  user-service:
    build: ./services/users
    environment:
      - DATABASE_URL=${USER_DATABASE_URL}
      - AUTH0_CONFIG=${AUTH0_CONFIG}
    deploy:
      replicas: 2

  # Background Processing
  celery-worker:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_CLUSTER=${REDIS_CLUSTER}
    deploy:
      replicas: 10

  # Monitoring & Observability
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"

volumes:
  grafana_data:
```

---

## AI Layer Architecture

### Multi-Provider Strategy
```python
# ai/providers.py
from litellm import completion
import os

class AIProvider:
    def __init__(self):
        self.providers = {
            'fast': 'groq/llama2-70b-4096',
            'quality': 'gpt-4-1106-preview',
            'cheap': 'gpt-3.5-turbo',
            'backup': 'claude-instant-1.2'
        }

    async def complete(self, prompt: str, provider_type: str = 'quality'):
        """Complete prompt with fallback strategy"""
        provider = self.providers[provider_type]

        try:
            # Try primary provider
            response = await completion(
                model=provider,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content

        except Exception as e:
            # Fallback to next provider
            return await self._fallback_completion(prompt, provider_type)

    async def _fallback_completion(self, prompt: str, failed_provider: str):
        """Implement fallback chain"""
        fallback_order = [
            'groq/llama2-70b-4096',
            'gpt-3.5-turbo',
            'claude-instant-1.2'
        ]

        for provider in fallback_order:
            if provider == failed_provider:
                continue

            try:
                response = await completion(
                    model=provider,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except:
                continue

        raise Exception("All AI providers failed")
```

### Cost Optimization
```python
# ai/cost_tracker.py
class CostTracker:
    def __init__(self):
        self.costs = {
            'gpt-4-1106-preview': 0.01,  # per 1K tokens
            'gpt-3.5-turbo': 0.002,
            'groq/llama2-70b-4096': 0.0007,
            'claude-instant-1.2': 0.0008
        }

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int):
        """Calculate API call cost"""
        if model not in self.costs:
            return 0

        input_cost = (input_tokens / 1000) * self.costs[model]
        output_cost = (output_tokens / 1000) * (self.costs[model] * 2)
        return input_cost + output_cost

    async def track_usage(self, user_id: str, model: str, cost: float):
        """Track usage by user"""
        # Store in database for billing
        await update_user_usage(user_id, model, cost)

        # Check usage limits
        await check_user_limits(user_id, cost)
```

---

## Security Implementation

### Authentication Flow
```typescript
// frontend/lib/auth.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export const supabase = createClientComponentClient()

export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  if (error) throw error
  return data
}

export const signUp = async (email: string, password: string, metadata?: any) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: metadata
    }
  })

  if (error) throw error
  return data
}
```

### Backend Security Middleware
```python
# backend/middleware/security.py
from fastapi import Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

def validate_supabase_jwt(request: Request):
    """Validate Supabase JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(" ")[1]
    try:
        # Validate with Supabase
        user = supabase_client.auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## Performance Optimization

### Frontend Optimization
```typescript
// next.config.js
const nextConfig = {
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', '@radix-ui/react-icons']
  },
  images: {
    domains: ['supabase.co'],
    formats: ['image/webp', 'image/avif']
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
  poweredByHeader: false,
  compress: true
}

module.exports = nextConfig
```

### Backend Performance
```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_redis_pool()
    await init_db_pool()
    yield
    # Shutdown
    await cleanup_resources()

app = FastAPI(
    title="Mindmesh API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Response caching
@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith("/api/tasks"):
        response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes
    elif request.url.path.startswith("/api/plans"):
        response.headers["Cache-Control"] = "public, max-age=600"  # 10 minutes

    return response
```

---

## Monitoring & Observability

### Frontend Monitoring
```typescript
// frontend/lib/monitoring.ts
import * as Sentry from '@sentry/nextjs'
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals'

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    environment: process.env.NODE_ENV,
  })
}

// Performance monitoring
function reportWebVitals(metric: any) {
  // Send to analytics
  gtag('event', metric.name, {
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
    event_category: 'Web Vitals',
    event_label: metric.id,
    non_interaction: true,
  })

  // Send to Sentry
  Sentry.addBreadcrumb({
    message: `Web Vital: ${metric.name}`,
    level: 'info',
    data: metric
  })
}

getCLS(reportWebVitals)
getFID(reportWebVitals)
getFCP(reportWebVitals)
getLCP(reportWebVitals)
getTTFB(reportWebVitals)
```

### Backend Monitoring
```python
# backend/monitoring.py
from prometheus_client import Counter, Histogram, Gauge
import time
import logging

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_USERS = Gauge('active_users_total', 'Number of active users')
AI_REQUESTS = Counter('ai_requests_total', 'Total AI requests', ['provider'])

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.File_handler('/var/log/mindmesh.log'),
        logging.StreamHandler()
    ]
)

# Performance monitoring decorator
def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            REQUEST_DURATION.observe(time.time() - start_time)
            return result
        except Exception as e:
            REQUEST_DURATION.observe(time.time() - start_time)
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper
```

---

## Environment Configuration

### Development Environment
```bash
# .env.local
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mindmesh

# Redis
REDIS_URL=redis://localhost:6379

# AI Providers
OPENAI_API_KEY=sk-openai-key
ANTHROPIC_API_KEY=sk-anthropic-key
GROQ_API_KEY=gsk_groq-key

# External Services
PUSHER_APP_ID=your_pusher_app_id
PUSHER_KEY=your_pusher_key
PUSHER_SECRET=your_pusher_secret

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

### Production Environment
```bash
# .env.production
# Same as development but with production values
# Additional security headers
SECURE_COOKIES=true
CSRF_PROTECTION=true
RATE_LIMITING_ENABLED=true

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_ADVANCED_AI=true
ENABLE_REALTIME=true

# Performance
CACHE_TTL=3600
MAX_WORKERS=10
```

---

## Deployment Strategy

### Vercel Configuration (Frontend)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase-url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase-anon-key"
  },
  "functions": {
    "pages/api/**/*.js": {
      "maxDuration": 30
    }
  }
}
```

### Railway Configuration (Backend)
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[services]
[services.api]
source = "."
name = "mindmesh-api"

[services.worker]
source = "."
name = "mindmesh-worker"
command = "celery -A app.celery worker --loglevel=info"
```

---

## Testing Strategy

### Frontend Testing
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@playwright/test": "^1.40.0",
    "msw": "^2.0.0"
  }
}
```

### Backend Testing
```python
# conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_db():
    # Setup test database
    setup_test_database()
    yield
    # Cleanup
    cleanup_test_database()

# Example test
@pytest.mark.asyncio
async def test_create_plan(client: AsyncClient, test_db):
    response = await client.post(
        "/api/plans",
        json={"title": "Test Plan", "description": "Test Description"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Plan"
```

---

## Scaling Strategy

### Horizontal Scaling
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mindmesh-backend
spec:
  replicas: 5
  selector:
    matchLabels:
      app: mindmesh-backend
  template:
    metadata:
      labels:
        app: mindmesh-backend
    spec:
      containers:
      - name: backend
        image: mindmesh/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mindmesh-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Database Scaling
```sql
-- Read replica configuration
-- In Supabase dashboard, enable read replicas
-- Connection string for reads:
DATABASE_URL_READ="postgresql://user:pass@db-read-replica:5432/mindmesh"

-- Optimized queries for scaling
CREATE INDEX CONCURRENTLY idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX CONCURRENTLY idx_plans_created_at ON plans(created_at DESC);
CREATE INDEX CONCURRENTLY idx_tasks_deadline ON tasks(deadline) WHERE deadline IS NOT NULL;
```

This comprehensive tech stack documentation provides everything needed to build, deploy, and scale Mindmesh from MVP to enterprise. The stack is designed to be cost-effective, maintainable, and scalable with clear progression paths for each growth phase.