import React from 'react';
import { Link } from 'react-router-dom';
import { Plus, Eye, Play } from 'lucide-react';
import { mockPatients } from '../data/mockData';

const Patients = () => {
  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-semibold text-primaryText">Patients</h2>
          <p className="text-mutedText mt-1">Manage patient profiles and eligibility analyses</p>
        </div>
        <Link
          to="/patients/new"
          className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4" />
          New Patient
        </Link>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <select className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary">
          <option>All Diagnoses</option>
          <option>Glioblastoma</option>
          <option>Alzheimer's</option>
          <option>Parkinson's</option>
        </select>
        <select className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary">
          <option>All Statuses</option>
          <option>Completed</option>
          <option>Processing</option>
          <option>Pending Review</option>
          <option>Failed</option>
        </select>
      </div>

      {/* Patient Table */}
      <div className="card overflow-hidden">
        <table className="w-full">
          <thead className="bg-secondary">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Patient ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Age</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Diagnosis</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Last Analysis</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Eligible Trials</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mutedText uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {mockPatients.map((patient) => (
              <tr key={patient.id} className="hover:bg-secondary transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primaryText">{patient.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-primaryText">
                  {patient.firstName} {patient.lastName}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-secondaryText">{patient.age}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-secondaryText">{patient.diagnosis}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-secondaryText">
                  {patient.lastAnalysis ? new Date(patient.lastAnalysis).toLocaleDateString() : 'Not analyzed'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-secondaryText">
                  {patient.status === 'Completed' ? '2 matches' : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    patient.status === 'Completed' ? 'bg-success/20 text-success' :
                    patient.status === 'Processing' ? 'bg-primary/20 text-primary' :
                    patient.status === 'Pending Review' ? 'bg-warning/20 text-warning' :
                    'bg-danger/20 text-danger'
                  }`}>
                    {patient.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <div className="flex gap-2">
                    <Link
                      to={`/patients/${patient.id}`}
                      className="p-1.5 text-secondaryText hover:text-primaryText transition-colors"
                      title="View"
                    >
                      <Eye className="w-4 h-4" />
                    </Link>
                    <Link
                      to={`/analysis/${patient.id}`}
                      className="p-1.5 text-secondaryText hover:text-primaryText transition-colors"
                      title="Analyze"
                    >
                      <Play className="w-4 h-4" />
                    </Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Patients;