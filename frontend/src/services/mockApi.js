// Mock API service for frontend development
// This will be replaced with real FastAPI calls later

import { mockPatients, mockTrials, mockMatchResults, mockProcessingSteps } from '../data/mockData';

// Simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Patient endpoints
export const getPatients = async () => {
  await delay(300);
  return mockPatients;
};

export const getPatient = async (id) => {
  await delay(200);
  return mockPatients.find(p => p.id === parseInt(id));
};

export const createPatient = async (patientData) => {
  await delay(500);
  const newPatient = {
    id: mockPatients.length + 1,
    ...patientData,
    createdAt: new Date().toISOString()
  };
  mockPatients.push(newPatient);
  return newPatient;
};

// MRI upload endpoints
export const uploadMRI = async (patientId, files) => {
  await delay(1000);
  return { success: true, message: 'MRI files uploaded successfully' };
};

// Clinical trial endpoints
export const getTrials = async () => {
  await delay(300);
  return mockTrials;
};

export const getTrial = async (id) => {
  await delay(200);
  return mockTrials.find(t => t.id === parseInt(id));
};

// Matching endpoints
export const matchPatientToTrials = async (patientId) => {
  await delay(2000);
  return mockMatchResults[patientId] || [];
};

export const getMatchResults = async (patientId) => {
  await delay(300);
  return mockMatchResults[patientId] || [];
};

// Processing endpoints
export const startProcessing = async (patientId) => {
  await delay(500);
  return { processingId: `proc-${Date.now()}`, status: 'started' };
};

export const getProcessingStatus = async (processingId) => {
  await delay(300);
  return {
    steps: mockProcessingSteps,
    status: 'in_progress',
    progress: 60
  };
};

// Reports endpoints
export const getReports = async () => {
  await delay(400);
  return {
    totalAnalyses: 183,
    averageMatchScore: 74,
    eligibleRate: 28,
    unknownRate: 16,
    eligibilityDistribution: {
      eligible: 37,
      uncertain: 18,
      notEligible: 42
    },
    matchingPerformance: {
      precision: 0.82,
      recall: 0.78,
      f1Score: 0.80,
      accuracy: 0.85
    },
    segmentationMetrics: {
      diceScore: 0.89,
      iou: 0.81,
      precision: 0.91,
      recall: 0.87
    }
  };
};

export default {
  getPatients,
  getPatient,
  createPatient,
  uploadMRI,
  getTrials,
  getTrial,
  matchPatientToTrials,
  getMatchResults,
  startProcessing,
  getProcessingStatus,
  getReports
};