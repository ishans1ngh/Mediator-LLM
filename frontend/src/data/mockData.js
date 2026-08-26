export const mockTrials = [
  {
    id: 'NCT01234567',
    title: 'Phase II Study of Novel Therapy in Glioblastoma',
    description: 'A randomized, double-blind, placebo-controlled study evaluating the efficacy and safety of a novel therapeutic agent in patients with newly diagnosed glioblastoma after standard chemoradiation.',
    phase: 'Phase II',
    status: 'Recruiting',
    condition: 'Glioblastoma',
    enrollment: '45/100',
    startDate: '2024-01-15',
    endDate: '2026-12-31',
    sponsor: 'NeuroTech Pharmaceuticals',
    principalInvestigator: 'Dr. Sarah Johnson',
    location: 'Multiple locations nationwide',
    eligibilityCriteria: [
      {
        criterion: 'Age ≥ 18',
        type: 'inclusion',
        patientValue: '52 years',
        requiredValue: '≥ 18 years',
        result: 'PASS',
        explanation: 'Patient age satisfies the minimum age requirement.'
      },
      {
        criterion: 'Confirmed glioblastoma diagnosis',
        type: 'inclusion',
        patientValue: 'Glioblastoma, Grade IV',
        requiredValue: 'Histologically confirmed glioblastoma',
        result: 'PASS',
        explanation: 'Patient has confirmed glioblastoma diagnosis.'
      },
      {
        criterion: 'Adequate renal function',
        type: 'inclusion',
        patientValue: 'Creatinine 0.9 mg/dL',
        requiredValue: 'Creatinine ≤ 1.5 mg/dL',
        result: 'PASS',
        explanation: 'Patient renal function within acceptable range.'
      },
      {
        criterion: 'Previous treatment with Drug X',
        type: 'exclusion',
        patientValue: 'Previous Drug X treatment',
        requiredValue: 'No prior Drug X therapy',
        result: 'FAIL',
        explanation: 'Patient has received prior treatment with Drug X.'
      },
      {
        criterion: 'ECOG Performance Status ≤ 2',
        type: 'inclusion',
        patientValue: 'Information unavailable',
        requiredValue: 'ECOG ≤ 2',
        result: 'UNKNOWN',
        explanation: 'ECOG performance status not documented in patient records.'
      }
    ],
    studyDesign: {
      type: 'Randomized, Double-blind, Placebo-controlled',
      duration: '24 months',
      visits: '12 scheduled visits',
      procedures: ['MRI scans', 'Cognitive testing', 'Blood work', 'Genetic testing']
    }
  },
  {
    id: 'NCT02345678',
    title: 'Immunotherapy for Recurrent Glioblastoma',
    description: 'Open-label study of checkpoint inhibitor therapy in patients with recurrent glioblastoma who have failed standard therapy.',
    phase: 'Phase I',
    status: 'Recruiting',
    condition: 'Glioblastoma',
    enrollment: '12/30',
    startDate: '2024-03-01',
    endDate: '2025-12-31',
    sponsor: 'ImmunoOncology Research',
    principalInvestigator: 'Dr. Michael Chen',
    location: '5 specialized cancer centers',
    eligibilityCriteria: [
      {
        criterion: 'Age ≥ 18',
        type: 'inclusion',
        patientValue: '52 years',
        requiredValue: '≥ 18 years',
        result: 'PASS',
        explanation: 'Patient age satisfies the minimum age requirement.'
      },
      {
        criterion: 'Recurrent glioblastoma',
        type: 'inclusion',
        patientValue: 'Glioblastoma, Grade IV',
        requiredValue: 'First or second recurrence',
        result: 'PASS',
        explanation: 'Patient meets recurrence criteria.'
      },
      {
        criterion: 'Previous immunotherapy',
        type: 'exclusion',
        patientValue: 'No prior immunotherapy',
        requiredValue: 'No prior checkpoint inhibitor therapy',
        result: 'PASS',
        explanation: 'Patient has not received prior immunotherapy.'
      },
      {
        criterion: 'Autoimmune disease',
        type: 'exclusion',
        patientValue: 'No autoimmune history',
        requiredValue: 'No active autoimmune disease',
        result: 'PASS',
        explanation: 'No autoimmune conditions documented.'
      }
    ],
    studyDesign: {
      type: 'Open-label, Single-arm',
      duration: '12 months',
      visits: '8 scheduled visits',
      procedures: ['MRI scans', 'Blood biomarkers', 'Immune profiling', 'Safety monitoring']
    }
  },
  {
    id: 'NCT03456789',
    title: 'Tumor Treating Fields in Newly Diagnosed GBM',
    description: 'Study evaluating the addition of tumor treating fields to standard chemoradiation in newly diagnosed glioblastoma patients.',
    phase: 'Phase III',
    status: 'Active',
    condition: 'Glioblastoma',
    enrollment: '78/200',
    startDate: '2023-06-01',
    endDate: '2027-06-30',
    sponsor: 'Medical Device Research',
    principalInvestigator: 'Dr. Emily Rodriguez',
    location: '15 sites across North America',
    eligibilityCriteria: [
      {
        criterion: 'Age ≥ 18',
        type: 'inclusion',
        patientValue: '52 years',
        requiredValue: '≥ 18 years',
        result: 'PASS',
        explanation: 'Patient age satisfies the minimum age requirement.'
      },
      {
        criterion: 'Newly diagnosed GBM',
        type: 'inclusion',
        patientValue: 'Glioblastoma, Grade IV',
        requiredValue: 'Newly diagnosed, untreated',
        result: 'FAIL',
        explanation: 'Patient has received prior treatment.'
      },
      {
        criterion: 'Adequate bone marrow function',
        type: 'inclusion',
        patientValue: 'ANC 1.8 × 10^9/L',
        requiredValue: 'ANC ≥ 1.5 × 10^9/L',
        result: 'PASS',
        explanation: 'Bone marrow function adequate.'
      }
    ],
    studyDesign: {
      type: 'Randomized, Controlled',
      duration: '24 months',
      visits: '16 scheduled visits',
      procedures: ['Device fitting', 'MRI scans', 'Blood work', 'Quality of life assessments']
    }
  }
];

export const mockPatients = [
  {
    id: 'PT-001',
    firstName: 'John',
    lastName: 'Smith',
    age: 52,
    gender: 'Male',
    dateOfBirth: '1972-03-15',
    diagnosis: 'Glioblastoma',
    stage: 'Grade IV',
    clinicalNotes: 'Patient diagnosed with glioblastoma in January 2024. Underwent surgical resection followed by concurrent chemoradiation with temozolomide. Currently on adjuvant temozolomide cycles. No significant comorbidities. Performance status appears good.',
    medicalHistory: 'Hypertension, well-controlled with medication. No history of other neurological conditions.',
    previousTreatments: ['Surgical resection', 'Radiation therapy', 'Temozolomide', 'Drug X'],
    currentMedications: ['Temozolomide', 'Lisinopril'],
    allergies: 'None known',
    performanceStatus: 'ECOG 1',
    labResults: {
      hemoglobin: { value: 13.2, unit: 'g/dL', reference: '12.0-16.0' },
      wbc: { value: 5.8, unit: '×10^9/L', reference: '4.5-11.0' },
      platelets: { value: 245, unit: '×10^9/L', reference: '150-400' },
      creatinine: { value: 0.9, unit: 'mg/dL', reference: '0.7-1.3' },
      alt: { value: 28, unit: 'U/L', reference: '7-56' },
      ast: { value: 24, unit: 'U/L', reference: '10-40' },
      bilirubin: { value: 0.8, unit: 'mg/dL', reference: '0.3-1.2' }
    },
    mri: {
      t1: true,
      t2: true,
      flair: true
    },
    createdAt: '2024-01-20T10:30:00Z',
    lastAnalysis: '2024-08-26T14:30:00Z',
    status: 'Completed'
  },
  {
    id: 'PT-002',
    firstName: 'Jane',
    lastName: 'Doe',
    age: 58,
    gender: 'Female',
    dateOfBirth: '1966-07-22',
    diagnosis: 'Glioblastoma',
    stage: 'Grade IV',
    clinicalNotes: 'Patient with newly diagnosed glioblastoma. Surgical resection completed 2 weeks ago. Planning to start chemoradiation. History of migraines but otherwise healthy.',
    medicalHistory: 'History of migraines, no significant neurological conditions',
    previousTreatments: ['Surgical resection'],
    currentMedications: ['Sumatriptan (as needed)'],
    allergies: 'Penicillin',
    performanceStatus: 'ECOG 0',
    labResults: {
      hemoglobin: { value: 12.8, unit: 'g/dL', reference: '12.0-16.0' },
      wbc: { value: 6.2, unit: '×10^9/L', reference: '4.5-11.0' },
      platelets: { value: 280, unit: '×10^9/L', reference: '150-400' },
      creatinine: { value: 0.8, unit: 'mg/dL', reference: '0.7-1.3' },
      alt: { value: 32, unit: 'U/L', reference: '7-56' },
      ast: { value: 28, unit: 'U/L', reference: '10-40' },
      bilirubin: { value: 0.6, unit: 'mg/dL', reference: '0.3-1.2' }
    },
    mri: {
      t1: true,
      t2: true,
      flair: false
    },
    createdAt: '2024-02-15T14:45:00Z',
    lastAnalysis: '2024-08-20T09:15:00Z',
    status: 'Processing'
  },
  {
    id: 'PT-003',
    firstName: 'Robert',
    lastName: 'Johnson',
    age: 67,
    gender: 'Male',
    dateOfBirth: '1957-11-08',
    diagnosis: 'Glioblastoma',
    stage: 'Grade IV',
    clinicalNotes: 'Elderly patient with glioblastoma. Due to age and comorbidities, received less aggressive treatment approach. Performance status declining.',
    medicalHistory: 'Type 2 diabetes, coronary artery disease, chronic kidney disease',
    previousTreatments: ['Surgical resection', 'Radiation therapy'],
    currentMedications: ['Metformin', 'Aspirin', 'Lisinopril'],
    allergies: 'Sulfa drugs',
    performanceStatus: 'ECOG 3',
    labResults: {
      hemoglobin: { value: 11.2, unit: 'g/dL', reference: '12.0-16.0' },
      wbc: { value: 4.2, unit: '×10^9/L', reference: '4.5-11.0' },
      platelets: { value: 180, unit: '×10^9/L', reference: '150-400' },
      creatinine: { value: 1.8, unit: 'mg/dL', reference: '0.7-1.3' },
      alt: { value: 45, unit: 'U/L', reference: '7-56' },
      ast: { value: 52, unit: 'U/L', reference: '10-40' },
      bilirubin: { value: 1.1, unit: 'mg/dL', reference: '0.3-1.2' }
    },
    mri: {
      t1: true,
      t2: false,
      flair: false
    },
    createdAt: '2024-03-10T16:20:00Z',
    lastAnalysis: null,
    status: 'Pending Review'
  }
];

export const mockMatchResults = {
  'PT-001': [
    {
      patientId: 'PT-001',
      trialId: 'NCT01234567',
      matchScore: 87,
      eligibility: 'ELIGIBLE',
      criteriaSatisfied: 4,
      totalCriteria: 5,
      criteria: [
        {
          criterion: 'Age ≥ 18',
          type: 'inclusion',
          patientValue: '52 years',
          requiredValue: '≥ 18 years',
          result: 'PASS',
          explanation: 'Patient age satisfies the minimum age requirement.'
        },
        {
          criterion: 'Confirmed glioblastoma diagnosis',
          type: 'inclusion',
          patientValue: 'Glioblastoma, Grade IV',
          requiredValue: 'Histologically confirmed glioblastoma',
          result: 'PASS',
          explanation: 'Patient has confirmed glioblastoma diagnosis.'
        },
        {
          criterion: 'Adequate renal function',
          type: 'inclusion',
          patientValue: 'Creatinine 0.9 mg/dL',
          requiredValue: 'Creatinine ≤ 1.5 mg/dL',
          result: 'PASS',
          explanation: 'Patient renal function within acceptable range.'
        },
        {
          criterion: 'Previous treatment with Drug X',
          type: 'exclusion',
          patientValue: 'Previous Drug X treatment',
          requiredValue: 'No prior Drug X therapy',
          result: 'FAIL',
          explanation: 'Patient has received prior treatment with Drug X.'
        },
        {
          criterion: 'ECOG Performance Status ≤ 2',
          type: 'inclusion',
          patientValue: 'Information unavailable',
          requiredValue: 'ECOG ≤ 2',
          result: 'UNKNOWN',
          explanation: 'ECOG performance status not documented in patient records.'
        }
      ],
      recommendations: 'Strong candidate overall. One exclusion criterion (prior Drug X) may need review. One criterion requires additional information.'
    },
    {
      patientId: 'PT-001',
      trialId: 'NCT02345678',
      matchScore: 92,
      eligibility: 'ELIGIBLE',
      criteriaSatisfied: 4,
      totalCriteria: 4,
      criteria: [
        {
          criterion: 'Age ≥ 18',
          type: 'inclusion',
          patientValue: '52 years',
          requiredValue: '≥ 18 years',
          result: 'PASS',
          explanation: 'Patient age satisfies the minimum age requirement.'
        },
        {
          criterion: 'Recurrent glioblastoma',
          type: 'inclusion',
          patientValue: 'Glioblastoma, Grade IV',
          requiredValue: 'First or second recurrence',
          result: 'PASS',
          explanation: 'Patient meets recurrence criteria.'
        },
        {
          criterion: 'Previous immunotherapy',
          type: 'exclusion',
          patientValue: 'No prior immunotherapy',
          requiredValue: 'No prior checkpoint inhibitor therapy',
          result: 'PASS',
          explanation: 'Patient has not received prior immunotherapy.'
        },
        {
          criterion: 'Autoimmune disease',
          type: 'exclusion',
          patientValue: 'No autoimmune history',
          requiredValue: 'No active autoimmune disease',
          result: 'PASS',
          explanation: 'No autoimmune conditions documented.'
        }
      ],
      recommendations: 'Excellent candidate. All criteria satisfied.'
    },
    {
      patientId: 'PT-001',
      trialId: 'NCT03456789',
      matchScore: 65,
      eligibility: 'NOT ELIGIBLE',
      criteriaSatisfied: 2,
      totalCriteria: 3,
      criteria: [
        {
          criterion: 'Age ≥ 18',
          type: 'inclusion',
          patientValue: '52 years',
          requiredValue: '≥ 18 years',
          result: 'PASS',
          explanation: 'Patient age satisfies the minimum age requirement.'
        },
        {
          criterion: 'Newly diagnosed GBM',
          type: 'inclusion',
          patientValue: 'Glioblastoma, Grade IV',
          requiredValue: 'Newly diagnosed, untreated',
          result: 'FAIL',
          explanation: 'Patient has received prior treatment.'
        },
        {
          criterion: 'Adequate bone marrow function',
          type: 'inclusion',
          patientValue: 'ANC 1.8 × 10^9/L',
          requiredValue: 'ANC ≥ 1.5 × 10^9/L',
          result: 'PASS',
          explanation: 'Bone marrow function adequate.'
        }
      ],
      recommendations: 'Not eligible due to prior treatment. Trial requires newly diagnosed, untreated patients.'
    }
  ]
};

export const mockProcessingSteps = [
  {
    id: 1,
    name: 'MRI Preprocessing',
    description: 'Normalizing and enhancing MRI scans for analysis',
    status: 'completed',
    duration: '1.2s',
    icon: 'Scan'
  },
  {
    id: 2,
    name: 'U-Net Segmentation',
    description: 'Segmenting tumor regions from brain tissue',
    status: 'completed',
    duration: '2.4s',
    icon: 'Brain'
  },
  {
    id: 3,
    name: 'ResNet-50 Feature Extraction',
    description: 'Extracting imaging features using deep learning',
    status: 'completed',
    duration: '1.8s',
    icon: 'Cpu'
  },
  {
    id: 4,
    name: 'Patient Reader Agent',
    description: 'Extracting structured information from clinical notes',
    status: 'in_progress',
    duration: null,
    icon: 'FileText',
    details: ['Diagnosis', 'Age', 'Treatment history', 'Laboratory values', 'Imaging features']
  },
  {
    id: 5,
    name: 'Clinical Trial Retrieval',
    description: 'Fetching relevant trials from ClinicalTrials.gov',
    status: 'pending',
    duration: null,
    icon: 'Database'
  },
  {
    id: 6,
    name: 'Trial Parser Agent',
    description: 'Parsing trial eligibility criteria into structured format',
    status: 'pending',
    duration: null,
    icon: 'FileJson'
  },
  {
    id: 7,
    name: 'Mediator Agent',
    description: 'Matching patient profile against trial criteria',
    status: 'pending',
    duration: null,
    icon: 'GitMerge'
  },
  {
    id: 8,
    name: 'Matching Evaluation',
    description: 'Generating final matching scores and recommendations',
    status: 'pending',
    duration: null,
    icon: 'CheckCircle'
  }
];
