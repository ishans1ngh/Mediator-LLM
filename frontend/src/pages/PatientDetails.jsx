import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Play, FileText, Activity } from 'lucide-react';
import { mockPatients } from '../data/mockData';

const PatientDetails = () => {
  const { id } = useParams();
  const patient = mockPatients.find(p => p.id === id);

  if (!patient) {
    return (
      <div className="text-center py-12">
        <p className="text-mutedText">Patient not found</p>
      </div>
    );
  }

  return (
    <div>
      {/* Back Button */}
      <Link
        to="/patients"
        className="flex items-center gap-2 text-secondaryText hover:text-primaryText mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Patients
      </Link>

      {/* Patient Header */}
      <div className="card p-6 mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-semibold text-primaryText mb-2">
              {patient.firstName} {patient.lastName}
            </h2>
            <p className="text-mutedText">{patient.id}</p>
          </div>
          <div className="flex gap-3">
            <Link
              to={`/analysis/${patient.id}`}
              className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              <Play className="w-4 h-4" />
              Start Analysis
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-4 gap-4 mt-6">
          <div>
            <p className="text-sm text-mutedText mb-1">Age</p>
            <p className="text-primaryText font-medium">{patient.age}</p>
          </div>
          <div>
            <p className="text-sm text-mutedText mb-1">Gender</p>
            <p className="text-primaryText font-medium">{patient.gender}</p>
          </div>
          <div>
            <p className="text-sm text-mutedText mb-1">Diagnosis</p>
            <p className="text-primaryText font-medium">{patient.diagnosis}</p>
          </div>
          <div>
            <p className="text-sm text-mutedText mb-1">Stage</p>
            <p className="text-primaryText font-medium">{patient.stage}</p>
          </div>
        </div>
      </div>

      {/* Patient Information */}
      <div className="grid grid-cols-2 gap-6">
        {/* Clinical Information */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold text-primaryText">Clinical Information</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm text-mutedText mb-1">Clinical Notes</p>
              <p className="text-secondaryText text-sm leading-relaxed">{patient.clinicalNotes}</p>
            </div>
            <div>
              <p className="text-sm text-mutedText mb-1">Medical History</p>
              <p className="text-secondaryText text-sm">{patient.medicalHistory}</p>
            </div>
            <div>
              <p className="text-sm text-mutedText mb-1">Previous Treatments</p>
              <div className="flex flex-wrap gap-2">
                {patient.previousTreatments.map((treatment, index) => (
                  <span key={index} className="px-2 py-1 bg-secondary text-secondaryText text-xs rounded">
                    {treatment}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <p className="text-sm text-mutedText mb-1">Current Medications</p>
              <div className="flex flex-wrap gap-2">
                {patient.currentMedications.map((med, index) => (
                  <span key={index} className="px-2 py-1 bg-secondary text-secondaryText text-xs rounded">
                    {med}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Lab Results & MRI */}
        <div className="space-y-6">
          {/* Lab Results */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-5 h-5 text-cyan" />
              <h3 className="text-lg font-semibold text-primaryText">Lab Results</h3>
            </div>
            
            <div className="space-y-3">
              {Object.entries(patient.labResults).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center py-2 border-b border-border last:border-0">
                  <div>
                    <p className="text-sm text-primaryText capitalize">{key}</p>
                    <p className="text-xs text-mutedText">Ref: {value.reference}</p>
                  </div>
                  <p className="text-sm font-medium text-primaryText">
                    {value.value} {value.unit}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* MRI Status */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-primaryText mb-4">MRI Scans</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-secondaryText">T1</span>
                <span className={`text-xs font-medium ${patient.mri.t1 ? 'text-success' : 'text-mutedText'}`}>
                  {patient.mri.t1 ? '✓ Uploaded' : 'Not uploaded'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-secondaryText">T2</span>
                <span className={`text-xs font-medium ${patient.mri.t2 ? 'text-success' : 'text-mutedText'}`}>
                  {patient.mri.t2 ? '✓ Uploaded' : 'Not uploaded'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-secondaryText">FLAIR</span>
                <span className={`text-xs font-medium ${patient.mri.flair ? 'text-success' : 'text-mutedText'}`}>
                  {patient.mri.flair ? '✓ Uploaded' : 'Not uploaded'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDetails;