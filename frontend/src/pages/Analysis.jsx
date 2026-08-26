import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, Clock, XCircle, Brain, Scan, Cpu, FileText, Database, FileJson, GitMerge } from 'lucide-react';
import { mockPatients, mockProcessingSteps } from '../data/mockData';

const Analysis = () => {
  const { patientId } = useParams();
  const [currentStep, setCurrentStep] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    const foundPatient = mockPatients.find(p => p.id === patientId);
    setPatient(foundPatient);

    // Simulate pipeline progression
    const timer = setInterval(() => {
      setCurrentStep(prev => {
        if (prev >= mockProcessingSteps.length - 1) {
          clearInterval(timer);
          setIsComplete(true);
          return prev;
        }
        return prev + 1;
      });
    }, 2000);

    return () => clearInterval(timer);
  }, [patientId]);

  const getIcon = (iconName) => {
    const icons = {
      Scan, Brain, Cpu, FileText, Database, FileJson, GitMerge, CheckCircle
    };
    const Icon = icons[iconName] || FileText;
    return <Icon className="w-6 h-6" />;
  };

  const getStatusIcon = (status, index) => {
    if (status === 'completed') {
      return <CheckCircle className="w-5 h-5 text-success" />;
    } else if (status === 'in_progress') {
      return <Clock className="w-5 h-5 text-primary animate-spin" />;
    } else {
      return <div className="w-5 h-5 rounded-full border-2 border-mutedText" />;
    }
  };

  if (!patient) {
    return (
      <div className="text-center py-12">
        <p className="text-mutedText">Patient not found</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-primaryText mb-2">Analyzing Patient</h2>
        <p className="text-mutedText">{patient.id} - {patient.diagnosis}</p>
      </div>

      {/* Pipeline */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-primaryText mb-6">Analysis Pipeline</h3>
        
        <div className="space-y-4">
          {mockProcessingSteps.map((step, index) => {
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;
            const isPending = index > currentStep;
            
            let status = 'pending';
            if (isCompleted) status = 'completed';
            else if (isActive) status = 'in_progress';

            return (
              <div
                key={step.id}
                className={`flex items-start gap-4 p-4 rounded-lg transition-all ${
                  isActive ? 'bg-primary/10 border border-primary' :
                  isCompleted ? 'bg-success/10 border border-success' :
                  'bg-secondary border border-border'
                }`}
              >
                {/* Status Icon */}
                <div className="flex-shrink-0 mt-1">
                  {getStatusIcon(status, index)}
                </div>

                {/* Content */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    {getIcon(step.icon)}
                    <h4 className="font-medium text-primaryText">{step.name}</h4>
                    {step.duration && (
                      <span className="text-xs text-mutedText">{step.duration}</span>
                    )}
                  </div>
                  <p className="text-sm text-secondaryText mb-2">{step.description}</p>
                  
                  {step.details && isActive && (
                    <div className="mt-2 p-3 bg-secondary rounded">
                      <p className="text-xs text-mutedText mb-2">Extracting:</p>
                      <div className="flex flex-wrap gap-2">
                        {step.details.map((detail, i) => (
                          <span key={i} className="text-xs text-primaryText bg-primary/20 px-2 py-1 rounded">
                            {detail}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Completion */}
        {isComplete && (
          <div className="mt-8 p-6 bg-success/10 border border-success rounded-lg text-center">
            <CheckCircle className="w-12 h-12 text-success mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-primaryText mb-2">Analysis Complete</h3>
            <p className="text-secondaryText mb-4">3 clinical trials evaluated</p>
            <Link
              to={`/results/${patientId}`}
              className="inline-flex items-center gap-2 px-6 py-3 bg-success hover:bg-green-600 text-white rounded-lg transition-colors"
            >
              View Matching Results
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analysis;