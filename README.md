# Mediator LLM - Clinical Trial Matching System

A web application that matches patients to clinical trials using AI and medical imaging analysis.

## Project Structure

```
Mediator-LLM/
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service layer
│   │   ├── data/         # Mock data
│   │   ├── App.jsx       # Main app component
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── backend/              # Express backend API
    ├── server.js         # Main server file
    └── package.json
```

## Frontend Components

### Components
- **Navbar.jsx** - Navigation bar
- **Sidebar.jsx** - Sidebar with trial list
- **PatientForm.jsx** - Patient registration form
- **MRIUploader.jsx** - MRI file upload component
- **TrialCard.jsx** - Clinical trial card display
- **CriterionCard.jsx** - Eligibility criterion card
- **StatusBadge.jsx** - Status badge component
- **LoadingPipeline.jsx** - Processing pipeline visualization

### Pages
- **Dashboard.jsx** - Main dashboard with trial overview
- **NewPatient.jsx** - New patient registration
- **Processing.jsx** - Data processing pipeline
- **Results.jsx** - Clinical trial matching results
- **TrialDetails.jsx** - Detailed trial information

## Getting Started

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:3000`

### Backend Setup

```bash
cd backend
npm install
npm start
```

The backend API will run on `http://localhost:5000`

## Features

- Patient registration and medical history management
- MRI scan upload and processing
- AI-powered clinical trial matching
- Real-time processing pipeline visualization
- Comprehensive eligibility criteria evaluation
- Detailed clinical trial information

## Technology Stack

### Frontend
- React 18
- React Router
- Vite
- CSS3

### Backend
- Express.js
- Node.js
- CORS support

## API Endpoints

- `GET /api/trials` - Get all clinical trials
- `GET /api/trials/:id` - Get specific trial details
- `POST /api/patients` - Create new patient
- `POST /api/mri/upload` - Upload MRI scans
- `POST /api/matching/:patientId` - Match patient to trials
- `POST /api/processing/start` - Start processing pipeline
- `GET /api/processing/status/:id` - Get processing status

## License

ISC
