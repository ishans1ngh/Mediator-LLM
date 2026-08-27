# Mediator LLM Backend

FastAPI backend for the AI-Powered Clinical Trial Matching system.

## Project Overview

This backend provides a REST API for clinical trial patient matching, integrating with ClinicalTrials.gov and providing a foundation for AI-powered analysis through patient reading, trial parsing, and mediator agents.

## Architecture

```
React Frontend
      │
      │ REST
      ▼
FastAPI API
      │
┌─────┼─────┐
│     │     │
▼     ▼     ▼
Patients Trials Analysis
│     │     │
│     ▼     │
│ ClinicalTrials.gov
│           │
▼           ▼
PostgreSQL  Analysis Service
                  │
   ┌──────────────┼──────────────┐
   │              │              │
   ▼              ▼              ▼
Imaging Stub  Patient Reader  Trial Parser
                              │
                              ▼
                        Mediator Stub
                              │
                              ▼
                      Matching Results
                              │
                              ▼
                        PostgreSQL
```

## Technology Stack

- **Python 3.11+**
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **PostgreSQL** - Database
- **SQLAlchemy 2.x** - ORM
- **Alembic** - Database migrations
- **Pydantic / Pydantic Settings** - Data validation and configuration
- **httpx** - Async HTTP client
- **psycopg** - PostgreSQL driver

## Requirements

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
APP_NAME=Mediator LLM
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/mediator_llm

CLINICALTRIALS_API_URL=https://clinicaltrials.gov/api/v2

UPLOAD_DIR=./uploads

MAX_UPLOAD_SIZE_MB=500

CORS_ORIGINS=http://localhost:5173,http://localhost:3000

TRIAL_CANDIDATE_LIMIT=20
ANALYSIS_STEP_DELAY_SECONDS=0.35
HTTP_TIMEOUT_SECONDS=15
```

## Local Setup

### 1. PostgreSQL Setup

Install PostgreSQL and create a database:

```bash
# Using psql
createdb mediator_llm
```

Or use Docker:

```bash
docker run -d \
  --name mediator_llm_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mediator_llm \
  -p 5432:5432 \
  postgres:16-alpine
```

### 2. Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Migrations

```bash
alembic upgrade head
```

### 5. Seed Database (Optional)

```bash
python -m app.seed
```

This creates synthetic data for development:
- 10 patients
- 20 trials
- 5 completed analyses with matching results

### 6. Run FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 7. API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Setup

### Using Docker Compose

```bash
cd backend
docker compose up
```

This starts:
- PostgreSQL on port 5432
- FastAPI backend on port 8000

### Manual Docker Build

```bash
docker build -t mediator-llm-backend .
docker run -p 8000:8000 --env-file .env mediator-llm-backend
```

## API Endpoints

### Health

- `GET /api/v1/health` - Health check
- `GET /api/v1/health/db` - Database health check

### Patients

- `POST /api/v1/patients` - Create patient
- `GET /api/v1/patients` - List patients (with pagination, search, filters)
- `GET /api/v1/patients/{patient_id}` - Get patient details
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `DELETE /api/v1/patients/{patient_id}` - Delete patient

### Labs

- `POST /api/v1/patients/{patient_id}/labs` - Add lab result
- `GET /api/v1/patients/{patient_id}/labs` - List lab results
- `DELETE /api/v1/patients/{patient_id}/labs/{lab_id}` - Delete lab result

### Treatments

- `POST /api/v1/patients/{patient_id}/treatments` - Add treatment
- `GET /api/v1/patients/{patient_id}/treatments` - List treatments
- `DELETE /api/v1/patients/{patient_id}/treatments/{treatment_id}` - Delete treatment

### Imaging

- `POST /api/v1/patients/{patient_id}/mri` - Upload MRI scan (multipart form-data)

### Trials

- `GET /api/v1/trials` - List trials (with filters)
- `GET /api/v1/trials/search` - Search ClinicalTrials.gov and sync
- `GET /api/v1/trials/{trial_id}` - Get trial details
- `GET /api/v1/trials/nct/{nct_id}` - Get trial by NCT ID
- `POST /api/v1/trials/sync` - Sync trials from ClinicalTrials.gov
- `GET /api/v1/trials/{trial_id}/criteria` - Get trial eligibility criteria
- `POST /api/v1/trials/{trial_id}/criteria/parse` - Parse trial eligibility criteria

### Analysis

- `POST /api/v1/analyses` - Create analysis (starts pipeline)
- `GET /api/v1/analyses/{analysis_id}` - Get analysis
- `GET /api/v1/analyses/{analysis_id}/status` - Get analysis status and progress
- `GET /api/v1/analyses/{analysis_id}/results` - Get matching results

### Matching

- `GET /api/v1/matching-results/{result_id}` - Get detailed matching result with criterion evaluations

## Example API Calls

### Create Patient

```bash
curl -X POST http://localhost:8000/api/v1/patients \
  -H "Content-Type: application/json" \
  -d '{
    "patient_code": "PT-001",
    "name": "Demo Patient",
    "age": 52,
    "gender": "Male",
    "diagnosis": "Glioblastoma",
    "disease_stage": "Grade IV",
    "clinical_notes": "Synthetic notes",
    "medical_history": "Synthetic history",
    "performance_status": "ECOG 1"
  }'
```

### List Patients

```bash
curl http://localhost:8000/api/v1/patients?page=1&page_size=20
```

### Upload MRI

```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_id}/mri \
  -F "file=@mri_scan.dcm" \
  -F "modality=T1"
```

### Sync Trials

```bash
curl -X POST "http://localhost:8000/api/v1/trials/sync?condition=Glioblastoma&max_results=20"
```

### Search Trials

```bash
curl "http://localhost:8000/api/v1/trials/search?condition=Glioblastoma&max_results=20"
```

### Get Trial Criteria

```bash
curl http://localhost:8000/api/v1/trials/{trial_id}/criteria
```

### Parse Trial Criteria

```bash
curl -X POST http://localhost:8000/api/v1/trials/{trial_id}/criteria/parse
```

### Create Analysis

```bash
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "uuid-here"}'
```

### Get Analysis Status

```bash
curl http://localhost:8000/api/v1/analyses/{analysis_id}/status
```

## Database Schema

### Tables

- `patients` - Patient records
- `patient_profile_attributes` - Extracted patient attributes
- `patient_labs` - Lab results
- `patient_treatments` - Treatment history
- `patient_mri_scans` - MRI scan metadata
- `trials` - Clinical trial records
- `trial_criteria` - Structured eligibility criteria
- `analyses` - Analysis jobs
- `analysis_steps` - Analysis pipeline steps
- `matching_results` - Trial matching results
- `criterion_evaluations` - Per-criterion evaluations

### Relationships

```
Patient
 ├── Profile Attributes
 ├── Labs
 ├── Treatments
 ├── MRI Scans
 └── Analyses

Trial
 └── Criteria

Analysis
 ├── Steps
 └── Matching Results

Matching Result
 └── Criterion Evaluations
```

## Analysis Pipeline

The analysis pipeline runs asynchronously with the following steps:

1. **MRI_PREPROCESSING** - Preprocess MRI scans (stub)
2. **UNET_SEGMENTATION** - Tumor segmentation (stub)
3. **RESNET_FEATURE_EXTRACTION** - Feature extraction (stub)
4. **PATIENT_READER** - Extract patient attributes (mock agent)
5. **TRIAL_RETRIEVAL** - Retrieve candidate trials from ClinicalTrials.gov
6. **TRIAL_PARSER** - Parse eligibility criteria (mock agent)
7. **STRUCTURED_CRITERIA** - Structure criteria for evaluation
8. **MEDIATOR** - Evaluate patient against criteria (mock agent)
9. **MATCHING_EVALUATION** - Generate final matching results

## ClinicalTrials.gov Integration

The backend integrates with ClinicalTrials.gov API v2 to retrieve and normalize clinical trial data.

### Data Flow

```
ClinicalTrials.gov API
        ↓
ClinicalTrials Service
        ↓
Normalizer
        ↓
Trial Service
        ↓
PostgreSQL
        ↓
Eligibility Text
        ↓
Deterministic Parser
        ↓
Trial Criteria
```

### Features

- **External API Integration**: Async HTTP client with timeout and error handling
- **Normalization**: Converts external API responses to internal schema
- **Upsert**: Prevents duplicate trials by NCT ID
- **Eligibility Parsing**: Deterministic parser for common patterns (age, sex, diagnosis)
- **Parser Interface**: Replaceable design for future LLM-based parser
- **Structured Criteria**: Stores both structured and unstructured criteria

### Deterministic Parser

The current parser handles simple patterns:
- Age: "Age >= 18", "at least 18 years", "18 years or older"
- Sex: "Male", "Female"
- Diagnosis: "confirmed glioblastoma", "histologically confirmed"

Complex criteria remain unstructured for future LLM processing.

### Parser Status

- **STRUCTURED**: Successfully parsed into field/operator/value
- **UNSTRUCTURED**: Could not be confidently parsed, preserved as text

### Example Usage

```bash
# Search and sync trials
curl "http://localhost:8000/api/v1/trials/search?condition=Glioblastoma&max_results=20"

# Sync without returning results
curl -X POST "http://localhost:8000/api/v1/trials/sync?condition=Glioblastoma&max_results=20"

# Parse eligibility criteria
curl -X POST http://localhost:8000/api/v1/trials/{trial_id}/criteria/parse
```

## Agents

### Patient Reader Agent

Extracts structured attributes from patient data. Currently a deterministic mock implementation.

### Trial Parser Agent

Parses eligibility criteria into structured format. Currently uses deterministic parser with replaceable interface for future LLM implementation.

### Mediator Agent

Evaluates patient attributes against trial criteria. Currently uses deterministic rules.

## Frontend Integration

The frontend API service (`frontend/src/services/api.js`) is configured to use the FastAPI backend.

Set the API URL in the frontend `.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Testing

Run tests:

```bash
pytest
```

Tests cover:
- Health endpoints
- Patient CRUD operations
- Lab and treatment management
- Trial operations

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   ├── exceptions.py      # Custom exceptions
│   │   ├── logging.py         # Logging configuration
│   │   └── security.py        # Security utilities
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── api/
│   │   ├── router.py          # API router
│   │   └── endpoints/         # API endpoints
│   ├── services/              # Business logic
│   ├── repositories/          # Data access layer
│   ├── agents/                # AI agents (stubs)
│   └── utils/                 # Utilities
├── migrations/                # Alembic migrations
├── tests/                    # Test suite
├── uploads/                   # File storage
├── requirements.txt
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Development Notes

- All business logic is in services, not API routes
- Use repositories for database access
- Agents are designed to be replaceable with LLM implementations
- MRI processing is currently stubbed
- ClinicalTrials.gov integration includes timeout and error handling
- File uploads are validated for size and type
- CORS is configured for development origins

## Next Phase

The next development phase will replace the stub agents with real LLM implementations:
- Patient Reader Agent with actual text extraction
- Trial Parser Agent with NLP-based criteria parsing
- Mediator Agent with AI-powered eligibility evaluation
- Real U-Net and ResNet-50 imaging pipeline

## Troubleshooting

### Database Connection Issues

Check that PostgreSQL is running and the `DATABASE_URL` is correct.

### Migration Errors

If migrations fail, check that the database exists and credentials are correct.

### CORS Errors

Ensure the frontend URL is in `CORS_ORIGINS` in `.env`.

### File Upload Errors

Check `UPLOAD_DIR` exists and is writable. Verify `MAX_UPLOAD_SIZE_MB` is sufficient.

## License

Proprietary - All rights reserved
