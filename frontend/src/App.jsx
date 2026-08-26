import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import Topbar from './components/layout/Topbar';
import PageContainer from './components/layout/PageContainer';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import NewPatient from './pages/NewPatient';
import PatientDetails from './pages/PatientDetails';
import Analysis from './pages/Analysis';
import Results from './pages/Results';
import TrialDetails from './pages/TrialDetails';
import Trials from './pages/Trials';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <div className="main-content-wrapper">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={
              <>
                <Topbar title="Dashboard" />
                <PageContainer><Dashboard /></PageContainer>
              </>
            } />
            <Route path="/patients" element={
              <>
                <Topbar title="Patients" />
                <PageContainer title="Patients" subtitle="Manage patient profiles and eligibility analyses"><Patients /></PageContainer>
              </>
            } />
            <Route path="/patients/new" element={
              <>
                <Topbar title="New Patient" />
                <PageContainer title="Create New Patient"><NewPatient /></PageContainer>
              </>
            } />
            <Route path="/patients/:id" element={
              <>
                <Topbar title="Patient Details" />
                <PageContainer><PatientDetails /></PageContainer>
              </>
            } />
            <Route path="/analysis/:patientId" element={
              <>
                <Topbar title="Analysis" />
                <PageContainer><Analysis /></PageContainer>
              </>
            } />
            <Route path="/results/:patientId" element={
              <>
                <Topbar title="Matching Results" />
                <PageContainer><Results /></PageContainer>
              </>
            } />
            <Route path="/trials" element={
              <>
                <Topbar title="Clinical Trials" />
                <PageContainer title="Clinical Trials" subtitle="Search and explore clinical trials"><Trials /></PageContainer>
              </>
            } />
            <Route path="/trials/:id" element={
              <>
                <Topbar title="Trial Details" />
                <PageContainer><TrialDetails /></PageContainer>
              </>
            } />
            <Route path="/reports" element={
              <>
                <Topbar title="Reports" />
                <PageContainer title="Reports & Analytics" subtitle="System performance and metrics"><Reports /></PageContainer>
              </>
            } />
            <Route path="/settings" element={
              <>
                <Topbar title="Settings" />
                <PageContainer title="Settings" subtitle="Configure application preferences"><Settings /></PageContainer>
              </>
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
