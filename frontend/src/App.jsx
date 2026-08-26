import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
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

function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  return (
    <div className="app">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex min-h-screen min-w-0 flex-col lg:pl-[250px]">
        <Topbar onMenuClick={() => setSidebarOpen(true)} />
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<PageContainer><Dashboard /></PageContainer>} />
          <Route path="/patients" element={<PageContainer><Patients /></PageContainer>} />
          <Route path="/patients/new" element={<PageContainer title="Create New Patient"><NewPatient /></PageContainer>} />
          <Route path="/patients/:id" element={<PageContainer><PatientDetails /></PageContainer>} />
          <Route path="/analysis/:patientId" element={<PageContainer><Analysis /></PageContainer>} />
          <Route path="/results/:patientId" element={<PageContainer><Results /></PageContainer>} />
          <Route path="/trials" element={<PageContainer><Trials /></PageContainer>} />
          <Route path="/trials/:id" element={<PageContainer><TrialDetails /></PageContainer>} />
          <Route path="/reports" element={<PageContainer title="Reports & Analytics" subtitle="System performance and metrics"><Reports /></PageContainer>} />
          <Route path="/settings" element={<PageContainer title="Settings" subtitle="Configure application preferences"><Settings /></PageContainer>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppShell />
    </Router>
  );
}

export default App;
