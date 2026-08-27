const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = {
  // Health check
  health: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },

  // Patient endpoints
  getPatients: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/patients${queryString ? `?${queryString}` : ''}`);
    if (!response.ok) throw new Error('Failed to fetch patients');
    return response.json();
  },

  getPatient: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`);
    if (!response.ok) throw new Error('Failed to fetch patient');
    return response.json();
  },

  createPatient: async (patientData) => {
    const response = await fetch(`${API_BASE_URL}/patients`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) throw new Error('Failed to create patient');
    return response.json();
  },

  updatePatient: async (patientId, patientData) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    if (!response.ok) throw new Error('Failed to update patient');
    return response.json();
  },

  deletePatient: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete patient');
    return response.json();
  },

  extractPatientProfile: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/extract`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to extract patient profile');
    return response.json();
  },

  getPatientProfile: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/profile`);
    if (!response.ok) throw new Error('Failed to fetch patient profile');
    return response.json();
  },

  // Lab endpoints
  addLab: async (patientId, labData) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/labs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(labData),
    });
    if (!response.ok) throw new Error('Failed to add lab');
    return response.json();
  },

  getLabs: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/labs`);
    if (!response.ok) throw new Error('Failed to fetch labs');
    return response.json();
  },

  deleteLab: async (patientId, labId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/labs/${labId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete lab');
    return response.json();
  },

  // Treatment endpoints
  addTreatment: async (patientId, treatmentData) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/treatments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(treatmentData),
    });
    if (!response.ok) throw new Error('Failed to add treatment');
    return response.json();
  },

  getTreatments: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/treatments`);
    if (!response.ok) throw new Error('Failed to fetch treatments');
    return response.json();
  },

  deleteTreatment: async (patientId, treatmentId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/treatments/${treatmentId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete treatment');
    return response.json();
  },

  // MRI upload endpoints
  uploadMRI: async (patientId, file, modality) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('modality', modality);
    
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/mri`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to upload MRI');
    return response.json();
  },

  // Clinical trial endpoints
  getTrials: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/trials${queryString ? `?${queryString}` : ''}`);
    if (!response.ok) throw new Error('Failed to fetch trials');
    return response.json();
  },

  searchTrials: async (condition, maxResults = 20) => {
    const response = await fetch(`${API_BASE_URL}/trials/search?condition=${encodeURIComponent(condition)}&max_results=${maxResults}`);
    if (!response.ok) throw new Error('Failed to search trials');
    return response.json();
  },

  getTrial: async (trialId) => {
    const response = await fetch(`${API_BASE_URL}/trials/${trialId}`);
    if (!response.ok) throw new Error('Failed to fetch trial');
    return response.json();
  },

  getTrialByNct: async (nctId) => {
    const response = await fetch(`${API_BASE_URL}/trials/nct/${nctId}`);
    if (!response.ok) throw new Error('Failed to fetch trial');
    return response.json();
  },

  syncTrials: async (condition, maxResults = 20) => {
    const response = await fetch(`${API_BASE_URL}/trials/sync?condition=${encodeURIComponent(condition)}&max_results=${maxResults}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to sync trials');
    return response.json();
  },

  getTrialCriteria: async (trialId) => {
    const response = await fetch(`${API_BASE_URL}/trials/${trialId}/criteria`);
    if (!response.ok) throw new Error('Failed to fetch trial criteria');
    return response.json();
  },

  parseTrialCriteria: async (trialId) => {
    const response = await fetch(`${API_BASE_URL}/trials/${trialId}/criteria/parse`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to parse trial criteria');
    return response.json();
  },

  parseTrialWithAI: async (trialId) => {
    const response = await fetch(`${API_BASE_URL}/trials/${trialId}/parse`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to parse trial with AI');
    return response.json();
  },

  // Analysis endpoints
  createAnalysis: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/analyses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ patient_id: patientId }),
    });
    if (!response.ok) throw new Error('Failed to create analysis');
    return response.json();
  },

  getAnalysis: async (analysisId) => {
    const response = await fetch(`${API_BASE_URL}/analyses/${analysisId}`);
    if (!response.ok) throw new Error('Failed to fetch analysis');
    return response.json();
  },

  getAnalysisStatus: async (analysisId) => {
    const response = await fetch(`${API_BASE_URL}/analyses/${analysisId}/status`);
    if (!response.ok) throw new Error('Failed to fetch analysis status');
    return response.json();
  },

  getAnalysisResults: async (analysisId) => {
    const response = await fetch(`${API_BASE_URL}/analyses/${analysisId}/results`);
    if (!response.ok) throw new Error('Failed to fetch analysis results');
    return response.json();
  },

  getMatchingResultDetail: async (resultId) => {
    const response = await fetch(`${API_BASE_URL}/matching-results/${resultId}`);
    if (!response.ok) throw new Error('Failed to fetch matching result detail');
    return response.json();
  },
};

export default api;
