import React from 'react';
import { Link } from 'react-router-dom';
import { Plus, Users, ClipboardList, CheckCircle, AlertCircle, Activity } from 'lucide-react';
import { mockPatients } from '../data/mockData';

const Dashboard = () => {
  const stats = [
    { title: 'Total Patients', value: 128, icon: Users, trend: '+12% this month', bgClass: 'bg-primary/20', textClass: 'text-primary' },
    { title: 'Clinical Trials', value: 64, icon: ClipboardList, trend: '+8% this month', bgClass: 'bg-cyan/20', textClass: 'text-cyan' },
    { title: 'AI Analyses', value: 83, icon: Activity, trend: '+6% this month', bgClass: 'bg-info/20', textClass: 'text-info' },
    { title: 'Eligible Matches', value: 37, icon: CheckCircle, trend: '+15% this month', bgClass: 'bg-success/20', textClass: 'text-success' },
    { title: 'Pending Reviews', value: 8, icon: AlertCircle, trend: '-2% this month', bgClass: 'bg-warning/20', textClass: 'text-warning' },
  ];

  const matchingOverview = {
    eligible: 37,
    uncertain: 18,
    notEligible: 42
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="min-w-0">
          <h2 className="text-2xl font-semibold text-primaryText">Clinical Trial Matching</h2>
          <p className="text-mutedText mt-1">AI-powered patient eligibility analysis</p>
        </div>
        <Link
          to="/patients/new"
          className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors flex-shrink-0"
        >
          <Plus className="w-4 h-4" />
          New Patient
        </Link>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
        {stats.map((stat) => (
          <div key={stat.title} className="bg-card border border-border rounded-lg p-5 hover:border-primary/50 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stat.bgClass} flex-shrink-0`}>
                <stat.icon className={`w-5 h-5 ${stat.textClass}`} />
              </div>
            </div>
            <p className="text-sm text-mutedText mb-1">{stat.title}</p>
            <p className="text-2xl font-bold text-primaryText mb-2">{stat.value}</p>
            <p className={`text-xs ${stat.trend.startsWith('+') ? 'text-success' : 'text-danger'}`}>{stat.trend}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Patients */}
        <div className="lg:col-span-2 bg-card border border-border rounded-lg overflow-hidden">
          <div className="p-5 border-b border-border flex justify-between items-center">
            <h3 className="text-lg font-semibold text-primaryText">Recent Patients</h3>
            <Link to="/patients" className="text-sm text-primary hover:text-primary/80 transition-colors">
              View all →
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-secondary">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Patient ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Diagnosis</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Age</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Last Analysis</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Matches</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {mockPatients.slice(0, 5).map((patient) => (
                  <tr key={patient.id} className="hover:bg-card-hover transition-colors">
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-primary">
                      <Link to={`/patients/${patient.id}`} className="hover:text-primary/80 transition-colors">
                        {patient.id}
                      </Link>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-secondaryText">{patient.diagnosis}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-secondaryText">{patient.age}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-secondaryText">
                      {patient.lastAnalysis ? new Date(patient.lastAnalysis).toLocaleDateString() : 'Not analyzed'}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-secondaryText">
                      {patient.status === 'Completed' ? '2 matches' : '-'}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-full ${
                        patient.status === 'Completed' ? 'bg-success/20 text-success' :
                        patient.status === 'Processing' ? 'bg-primary/20 text-primary' :
                        patient.status === 'Pending Review' ? 'bg-warning/20 text-warning' :
                        'bg-danger/20 text-danger'
                      }`}>
                        <span className="w-1.5 h-1.5 rounded-full mr-1.5 ${
                          patient.status === 'Completed' ? 'bg-success' :
                          patient.status === 'Processing' ? 'bg-primary' :
                          patient.status === 'Pending Review' ? 'bg-warning' :
                          'bg-danger'
                        }"></span>
                        {patient.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Matching Overview */}
        <div className="bg-card border border-border rounded-lg p-5">
          <h3 className="text-lg font-semibold text-primaryText mb-4">Matching Overview</h3>
          
          <div className="space-y-4">
            <div className="bg-secondary p-4 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-secondaryText">Eligible</span>
                <span className="text-lg font-bold text-success">{matchingOverview.eligible}</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div className="bg-success h-2 rounded-full transition-all duration-500" style={{ width: '38%' }}></div>
              </div>
            </div>

            <div className="bg-secondary p-4 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-secondaryText">Uncertain</span>
                <span className="text-lg font-bold text-warning">{matchingOverview.uncertain}</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div className="bg-warning h-2 rounded-full transition-all duration-500" style={{ width: '19%' }}></div>
              </div>
            </div>

            <div className="bg-secondary p-4 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-secondaryText">Not Eligible</span>
                <span className="text-lg font-bold text-danger">{matchingOverview.notEligible}</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div className="bg-danger h-2 rounded-full transition-all duration-500" style={{ width: '43%' }}></div>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-success/10 border border-success/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
              <p className="text-sm font-medium text-primaryText">System Status</p>
            </div>
            <p className="text-xs text-secondaryText">All systems operational. AI agents running normally.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
