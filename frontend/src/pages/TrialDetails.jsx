import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Bookmark, Download, Mail, AlertCircle } from 'lucide-react';
import { getTrial } from '../services/mockApi';

const TrialDetails = () => {
  const { id } = useParams();
  const [trial, setTrial] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const fetchTrial = async () => {
      const trialData = await getTrial(id);
      setTrial(trialData);
    };
    fetchTrial();
  }, [id]);

  if (!trial) {
    return (
      <div className="text-center py-12">
        <p className="text-mutedText">Loading trial details...</p>
      </div>
    );
  }

  const getResultIcon = (result) => {
    switch (result) {
      case 'PASS':
        return <span className="text-success">✓</span>;
      case 'FAIL':
        return <span className="text-danger">✕</span>;
      case 'UNKNOWN':
        return <span className="text-warning">?</span>;
      default:
        return null;
    }
  };

  const getResultColor = (result) => {
    switch (result) {
      case 'PASS': return 'success';
      case 'FAIL': return 'danger';
      case 'UNKNOWN': return 'warning';
      default: return 'mutedText';
    }
  };

  return (
    <div>
      {/* Back Button */}
      <Link
        to="/trials"
        className="flex items-center gap-2 text-secondaryText hover:text-primaryText mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Clinical Trials
      </Link>

      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <p className="text-sm text-mutedText">{trial.id}</p>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${
              trial.status === 'Recruiting' ? 'bg-success/20 text-success' :
              trial.status === 'Active' ? 'bg-primary/20 text-primary' :
              'bg-mutedText/20 text-mutedText'
            }`}>
              {trial.status}
            </span>
            <span className="px-2 py-1 text-xs font-medium rounded-full bg-cyan/20 text-cyan">
              {trial.phase}
            </span>
          </div>
          <h1 className="text-2xl font-semibold text-primaryText mb-2">{trial.title}</h1>
          <p className="text-mutedText">{trial.condition}</p>
        </div>
        
        <button
          onClick={() => setSaved(!saved)}
          className={`p-2 rounded-lg transition-colors ${
            saved ? 'bg-primary text-white' : 'bg-card text-secondaryText hover:text-primaryText'
          }`}
        >
          <Bookmark className="w-5 h-5" />
        </button>
      </div>

      {/* Overview */}
      <div className="bg-card border border-border rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-primaryText mb-4">Overview</h3>
        <p className="text-secondaryText leading-relaxed mb-6">{trial.description}</p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Phase</p>
            <p className="text-primaryText font-medium">{trial.phase}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Enrollment</p>
            <p className="text-primaryText font-medium">{trial.enrollment}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Start Date</p>
            <p className="text-primaryText font-medium">{trial.startDate}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">End Date</p>
            <p className="text-primaryText font-medium">{trial.endDate}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Sponsor</p>
            <p className="text-primaryText font-medium">{trial.sponsor}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Principal Investigator</p>
            <p className="text-primaryText font-medium">{trial.principalInvestigator}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg col-span-2">
            <p className="text-sm text-mutedText mb-1">Location</p>
            <p className="text-primaryText font-medium">{trial.location}</p>
          </div>
        </div>
      </div>

      {/* Eligibility Criteria */}
      <div className="bg-card border border-border rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-primaryText mb-4">Eligibility Criteria</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Inclusion Criteria */}
          <div>
            <h4 className="font-medium text-primaryText mb-3">Inclusion Criteria</h4>
            <div className="space-y-3">
              {trial.eligibilityCriteria
                .filter(c => c.type === 'inclusion')
                .map((criterion, index) => (
                  <div key={index} className="p-3 bg-secondary rounded-lg">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-0.5">
                        {getResultIcon(criterion.result)}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-primaryText font-medium">{criterion.criterion}</p>
                        <p className="text-xs text-mutedText mt-1">Required: {criterion.requiredValue}</p>
                        {criterion.patientValue && (
                          <p className="text-xs text-secondaryText mt-1">Patient: {criterion.patientValue}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>

          {/* Exclusion Criteria */}
          <div>
            <h4 className="font-medium text-primaryText mb-3">Exclusion Criteria</h4>
            <div className="space-y-3">
              {trial.eligibilityCriteria
                .filter(c => c.type === 'exclusion')
                .map((criterion, index) => (
                  <div key={index} className="p-3 bg-secondary rounded-lg">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-0.5">
                        {getResultIcon(criterion.result)}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-primaryText font-medium">{criterion.criterion}</p>
                        <p className="text-xs text-mutedText mt-1">Required: {criterion.requiredValue}</p>
                        {criterion.patientValue && (
                          <p className="text-xs text-secondaryText mt-1">Patient: {criterion.patientValue}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Evidence Panel */}
        <div className="mt-6 p-4 bg-cyan/10 border border-cyan rounded-lg">
          <div className="flex items-start gap-2 mb-2">
            <AlertCircle className="w-4 h-4 text-cyan mt-0.5" />
            <p className="text-sm font-medium text-primaryText">Evidence Panel</p>
          </div>
          <p className="text-xs text-secondaryText">
            This panel shows the patient evidence for each criterion. PASS indicates the patient meets the criterion, 
            FAIL indicates they do not, and UNKNOWN indicates insufficient information to determine eligibility.
          </p>
        </div>
      </div>

      {/* Study Design */}
      <div className="bg-card border border-border rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-primaryText mb-4">Study Design</h3>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-mutedText mb-1">Design Type</p>
              <p className="text-primaryText">{trial.studyDesign.type}</p>
            </div>
            <div>
              <p className="text-sm text-mutedText mb-1">Duration</p>
              <p className="text-primaryText">{trial.studyDesign.duration}</p>
            </div>
            <div>
              <p className="text-sm text-mutedText mb-1">Scheduled Visits</p>
              <p className="text-primaryText">{trial.studyDesign.visits}</p>
            </div>
          </div>

          <div>
            <p className="text-sm text-mutedText mb-2">Procedures</p>
            <div className="flex flex-wrap gap-2">
              {trial.studyDesign.procedures.map((procedure, index) => (
                <span key={index} className="px-3 py-1 bg-secondary text-secondaryText text-sm rounded">
                  {procedure}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4">
        <button className="flex items-center gap-2 px-6 py-3 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors">
          <Bookmark className="w-4 h-4" />
          Save Trial
        </button>
        <button className="flex items-center gap-2 px-6 py-3 bg-secondary hover:bg-border text-primaryText rounded-lg transition-colors">
          <Download className="w-4 h-4" />
          Download Protocol
        </button>
        <button className="flex items-center gap-2 px-6 py-3 bg-secondary hover:bg-border text-primaryText rounded-lg transition-colors">
          <Mail className="w-4 h-4" />
          Contact Study Team
        </button>
      </div>

      {/* Disclaimer */}
      <div className="mt-8 p-4 bg-warning/10 border border-warning rounded-lg">
        <p className="text-sm text-warning">
          <strong>Research Prototype:</strong> This information is for research purposes only and should not be used for clinical decision-making.
        </p>
      </div>
    </div>
  );
};

export default TrialDetails;
