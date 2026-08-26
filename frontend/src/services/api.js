const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  // Patient endpoints
  createPatient: async (patientData) => {
    const response = await fetch(`${API_BASE_URL}/patients`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patientData),
    });
    return response.json();
  },

  getPatient: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}`);
    return response.json();
  },

  // MRI upload endpoints
  uploadMRI: async (formData) => {
    const response = await fetch(`${API_BASE_URL}/mri/upload`, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  },

  // Clinical trial endpoints
  getTrials: async () => {
    const response = await fetch(`${API_BASE_URL}/trials`);
    return response.json();
  },

  getTrial: async (trialId) => {
    const response = await fetch(`${API_BASE_URL}/trials/${trialId}`);
    return response.json();
  },

  // Matching endpoints
  matchPatientToTrials: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/matching/${patientId}`, {
      method: 'POST',
    });
    return response.json();
  },

  getMatchResults: async (matchId) => {
    const response = await fetch(`${API_BASE_URL}/matching/results/${matchId}`);
    return response.json();
  },

  // Processing endpoints
  startProcessing: async (patientId) => {
    const response = await fetch(`${API_BASE_URL}/processing/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ patientId }),
    });
    return response.json();
  },

  getProcessingStatus: async (processingId) => {
    const response = await fetch(`${API_BASE_URL}/processing/status/${processingId}`);
    return response.json();
  },
};

export default api;
