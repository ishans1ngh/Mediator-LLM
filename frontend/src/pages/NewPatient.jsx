import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Check, Upload } from 'lucide-react';
import { createPatient } from '../services/mockApi';

const NewPatient = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Patient Information
    patientId: '',
    age: '',
    gender: '',
    dateOfBirth: '',
    diagnosis: '',
    stage: '',
    
    // Step 2: Clinical Information
    primaryDiagnosis: '',
    clinicalNotes: '',
    medicalHistory: '',
    previousTreatments: '',
    currentMedications: '',
    allergies: '',
    performanceStatus: '',
    
    // Step 3: Lab Results
    labResults: {
      hemoglobin: { value: '', unit: 'g/dL', reference: '12.0-16.0' },
      wbc: { value: '', unit: '×10^9/L', reference: '4.5-11.0' },
      platelets: { value: '', unit: '×10^9/L', reference: '150-400' },
      creatinine: { value: '', unit: 'mg/dL', reference: '0.7-1.3' },
      alt: { value: '', unit: 'U/L', reference: '7-56' },
      ast: { value: '', unit: 'U/L', reference: '10-40' },
      bilirubin: { value: '', unit: 'mg/dL', reference: '0.3-1.2' }
    },
    
    // Step 4: MRI
    mri: {
      t1: null,
      t2: null,
      flair: null
    }
  });

  const steps = [
    { id: 1, title: 'Patient Information' },
    { id: 2, title: 'Clinical Information' },
    { id: 3, title: 'Lab Results' },
    { id: 4, title: 'MRI Upload' },
    { id: 5, title: 'Summary' }
  ];

  const handleNext = () => {
    if (step < steps.length) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      const patientData = {
        ...formData,
        firstName: 'New', // Will be replaced with actual form data
        lastName: 'Patient',
        previousTreatments: formData.previousTreatments.split(',').map(t => t.trim()),
        currentMedications: formData.currentMedications.split(',').map(m => m.trim()),
        mri: {
          t1: !!formData.mri.t1,
          t2: !!formData.mri.t2,
          flair: !!formData.mri.flair
        }
      };
      
      const newPatient = await createPatient(patientData);
      navigate(`/analysis/${newPatient.id}`);
    } catch (error) {
      console.error('Error creating patient:', error);
    }
  };

  const handleFileUpload = (scanType) => (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        mri: {
          ...prev.mri,
          [scanType]: file
        }
      }));
    }
  };

  const handleLabChange = (lab, value) => {
    setFormData(prev => ({
      ...prev,
      labResults: {
        ...prev.labResults,
        [lab]: {
          ...prev.labResults[lab],
          value
        }
      }
    }));
  };

  return (
    <div>
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((s, index) => (
            <React.Fragment key={s.id}>
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === s.id ? 'bg-primary text-white' :
                  step > s.id ? 'bg-success text-white' :
                  'bg-secondary text-mutedText'
                }`}>
                  {step > s.id ? <Check className="w-4 h-4" /> : s.id}
                </div>
                <span className={`ml-2 text-sm ${
                  step === s.id ? 'text-primaryText font-medium' :
                  step > s.id ? 'text-success' :
                  'text-mutedText'
                }`}>
                  {s.title}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div className={`flex-1 h-0.5 mx-4 ${
                  step > s.id ? 'bg-success' : 'bg-border'
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Form Content */}
      <div className="bg-card border border-border rounded-lg p-6">
        {step === 1 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-primaryText">Patient Information</h3>
            
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm text-mutedText mb-2">Patient ID</label>
                <input
                  type="text"
                  value={formData.patientId}
                  onChange={(e) => setFormData({...formData, patientId: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  placeholder="PT-XXX"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Age</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  placeholder="52"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({...formData, gender: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                >
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Date of Birth</label>
                <input
                  type="date"
                  value={formData.dateOfBirth}
                  onChange={(e) => setFormData({...formData, dateOfBirth: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Diagnosis</label>
                <input
                  type="text"
                  value={formData.diagnosis}
                  onChange={(e) => setFormData({...formData, diagnosis: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  placeholder="Glioblastoma"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Disease Stage</label>
                <input
                  type="text"
                  value={formData.stage}
                  onChange={(e) => setFormData({...formData, stage: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  placeholder="Grade IV"
                />
              </div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-primaryText">Clinical Information</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-mutedText mb-2">Primary Diagnosis</label>
                <input
                  type="text"
                  value={formData.primaryDiagnosis}
                  onChange={(e) => setFormData({...formData, primaryDiagnosis: e.target.value})}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  placeholder="Enter primary diagnosis"
                />
              </div>
              
              <div>
                <label className="block text-sm text-mutedText mb-2">Clinical Notes</label>
                <textarea
                  value={formData.clinicalNotes}
                  onChange={(e) => setFormData({...formData, clinicalNotes: e.target.value})}
                  rows={6}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary resize-none"
                  placeholder="Enter relevant clinical notes, diagnosis details, previous treatment history, symptoms, and other information relevant to clinical trial eligibility..."
                />
              </div>

              <div>
                <label className="block text-sm text-mutedText mb-2">Medical History</label>
                <textarea
                  value={formData.medicalHistory}
                  onChange={(e) => setFormData({...formData, medicalHistory: e.target.value})}
                  rows={3}
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary resize-none"
                  placeholder="Relevant medical history..."
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm text-mutedText mb-2">Previous Treatments</label>
                  <input
                    type="text"
                    value={formData.previousTreatments}
                    onChange={(e) => setFormData({...formData, previousTreatments: e.target.value})}
                    className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                    placeholder="Surgery, Radiation, Drug names (comma separated)"
                  />
                </div>
                <div>
                  <label className="block text-sm text-mutedText mb-2">Current Medications</label>
                  <input
                    type="text"
                    value={formData.currentMedications}
                    onChange={(e) => setFormData({...formData, currentMedications: e.target.value})}
                    className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                    placeholder="Medication names (comma separated)"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm text-mutedText mb-2">Allergies</label>
                  <input
                    type="text"
                    value={formData.allergies}
                    onChange={(e) => setFormData({...formData, allergies: e.target.value})}
                    className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                    placeholder="Known allergies"
                  />
                </div>
                <div>
                  <label className="block text-sm text-mutedText mb-2">Performance Status</label>
                  <select
                    value={formData.performanceStatus}
                    onChange={(e) => setFormData({...formData, performanceStatus: e.target.value})}
                    className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                  >
                    <option value="">Select ECOG status</option>
                    <option value="ECOG 0">ECOG 0 - Fully active</option>
                    <option value="ECOG 1">ECOG 1 - Restricted in physically strenuous activity</option>
                    <option value="ECOG 2">ECOG 2 - Ambulatory, unable to work</option>
                    <option value="ECOG 3">ECOG 3 - Limited self-care</option>
                    <option value="ECOG 4">ECOG 4 - Completely disabled</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-primaryText">Lab Results</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.entries(formData.labResults).map(([key, lab]) => (
                <div key={key} className="bg-secondary p-4 rounded-lg">
                  <label className="block text-sm text-primaryText mb-2 capitalize">{key}</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={lab.value}
                      onChange={(e) => handleLabChange(key, e.target.value)}
                      className="flex-1 px-3 py-2 bg-card border border-border rounded text-primaryText focus:outline-none focus:border-primary"
                      placeholder="Value"
                    />
                    <span className="px-3 py-2 bg-card border border-border rounded text-secondaryText text-sm">
                      {lab.unit}
                    </span>
                  </div>
                  <p className="text-xs text-mutedText mt-2">Reference: {lab.reference}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-primaryText">MRI Scans</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {['t1', 't2', 'flair'].map((scanType) => (
                <div key={scanType} className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-primary transition-colors">
                  <Upload className="w-8 h-8 text-mutedText mx-auto mb-4" />
                  <p className="text-sm font-medium text-primaryText mb-2 capitalize">Upload {scanType.toUpperCase()}</p>
                  <p className="text-xs text-mutedText mb-4">Drag & drop or browse</p>
                  <input
                    type="file"
                    accept=".dcm,.nii,.nii.gz,.png,.jpg,.jpeg"
                    onChange={handleFileUpload(scanType)}
                    className="hidden"
                    id={`mri-${scanType}`}
                  />
                  <label
                    htmlFor={`mri-${scanType}`}
                    className="inline-block px-4 py-2 bg-secondary hover:bg-border text-primaryText text-sm rounded-lg cursor-pointer transition-colors"
                  >
                    Browse Files
                  </label>
                  {formData.mri[scanType] && (
                    <p className="text-xs text-success mt-2">
                      ✓ {formData.mri[scanType].name}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {step === 5 && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-primaryText">Patient Summary</h3>
            
            <div className="bg-secondary p-6 rounded-lg space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-mutedText">Patient ID</p>
                  <p className="text-primaryText font-medium">{formData.patientId || 'Not specified'}</p>
                </div>
                <div>
                  <p className="text-sm text-mutedText">Age</p>
                  <p className="text-primaryText font-medium">{formData.age || 'Not specified'}</p>
                </div>
                <div>
                  <p className="text-sm text-mutedText">Diagnosis</p>
                  <p className="text-primaryText font-medium">{formData.diagnosis || 'Not specified'}</p>
                </div>
                <div>
                  <p className="text-sm text-mutedText">Stage</p>
                  <p className="text-primaryText font-medium">{formData.stage || 'Not specified'}</p>
                </div>
              </div>

              <div className="border-t border-border pt-4">
                <p className="text-sm font-medium text-primaryText mb-3">Clinical Information</p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-success" />
                    <span className="text-sm text-secondaryText">
                      {formData.clinicalNotes ? 'Clinical notes provided' : 'Clinical notes missing'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-success" />
                    <span className="text-sm text-secondaryText">
                      {formData.medicalHistory ? 'Medical history provided' : 'Medical history missing'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-success" />
                    <span className="text-sm text-secondaryText">
                      {Object.values(formData.labResults).some(lab => lab.value) ? 'Lab results provided' : 'Lab results missing'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t border-border pt-4">
                <p className="text-sm font-medium text-primaryText mb-3">MRI</p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Check className={`w-4 h-4 ${formData.mri.t1 ? 'text-success' : 'text-mutedText'}`} />
                    <span className="text-sm text-secondaryText">
                      T1 {formData.mri.t1 ? 'uploaded' : 'not uploaded'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className={`w-4 h-4 ${formData.mri.t2 ? 'text-success' : 'text-mutedText'}`} />
                    <span className="text-sm text-secondaryText">
                      T2 {formData.mri.t2 ? 'uploaded' : 'not uploaded'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className={`w-4 h-4 ${formData.mri.flair ? 'text-success' : 'text-mutedText'}`} />
                    <span className="text-sm text-secondaryText">
                      FLAIR {formData.mri.flair ? 'uploaded' : 'not uploaded'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t border-border">
          <button
            onClick={handleBack}
            disabled={step === 1}
            className="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-border text-primaryText rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
            Back
          </button>

          {step < steps.length ? (
            <button
              onClick={handleNext}
              className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              className="flex items-center gap-2 px-6 py-2 bg-success hover:bg-green-600 text-white rounded-lg transition-colors"
            >
              <Upload className="w-4 h-4" />
              Start Analysis
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default NewPatient;
