import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Filter, ChevronDown } from 'lucide-react';
import { getMatchResults, getTrials } from '../services/mockApi';
import { mockPatients } from '../data/mockData';

const Results = () => {
  const { patientId } = useParams();
  const [results, setResults] = useState([]);
  const [trials, setTrials] = useState([]);
  const [filter, setFilter] = useState('All');
  const [sortBy, setSortBy] = useState('Best Match');
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const matchResults = await getMatchResults(patientId);
      const allTrials = await getTrials();
      const foundPatient = mockPatients.find(p => p.id === patientId);
      
      setResults(matchResults);
      setTrials(allTrials);
      setPatient(foundPatient);
    };
    
    fetchData();
  }, [patientId]);

  const filteredResults = results.filter(result => {
    if (filter === 'All') return true;
    return result.eligibility === filter.toUpperCase();
  });

  const sortedResults = [...filteredResults].sort((a, b) => {
    if (sortBy === 'Best Match') return b.matchScore - a.matchScore;
    if (sortBy === 'Eligibility') {
      const order = { 'ELIGIBLE': 0, 'UNCERTAIN': 1, 'NOT ELIGIBLE': 2 };
      return order[a.eligibility] - order[b.eligibility];
    }
    return 0;
  });

  const getEligibilityColor = (eligibility) => {
    switch (eligibility) {
      case 'ELIGIBLE': return 'success';
      case 'UNCERTAIN': return 'warning';
      case 'NOT ELIGIBLE': return 'danger';
      default: return 'mutedText';
    }
  };

  const getMatchScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
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
      {/* Back Button */}
      <Link
        to="/patients"
        className="flex items-center gap-2 text-secondaryText hover:text-primaryText mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Patients
      </Link>

      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-primaryText mb-2">Clinical Trial Matching Results</h2>
        <p className="text-mutedText">Patient: {patient.id} - {patient.diagnosis}</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Eligible</p>
          <p className="text-3xl font-bold text-success">{results.filter(r => r.eligibility === 'ELIGIBLE').length}</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Uncertain</p>
          <p className="text-3xl font-bold text-warning">{results.filter(r => r.eligibility === 'UNCERTAIN').length}</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Not Eligible</p>
          <p className="text-3xl font-bold text-danger">{results.filter(r => r.eligibility === 'NOT ELIGIBLE').length}</p>
        </div>
      </div>

      {/* Filters and Sort */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex gap-4">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary"
          >
            <option value="All">All</option>
            <option value="Eligible">Eligible</option>
            <option value="Uncertain">Uncertain</option>
            <option value="Not Eligible">Not Eligible</option>
          </select>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-sm text-mutedText">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary"
          >
            <option value="Best Match">Best Match</option>
            <option value="Eligibility">Eligibility</option>
          </select>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-6">
        {sortedResults.map((result) => {
          const trial = trials.find(t => t.id === result.trialId);
          if (!trial) return null;

          return (
            <div key={result.trialId} className="card overflow-hidden">
              {/* Trial Header */}
              <div className="p-6 border-b border-border">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <p className="text-xs text-mutedText">{trial.id}</p>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full bg-${getEligibilityColor(result.eligibility)}/20 text-${getEligibilityColor(result.eligibility)}`}>
                        {result.eligibility}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-primaryText mb-2">{trial.title}</h3>
                    <div className="flex gap-4 text-sm text-secondaryText">
                      <span>{trial.phase}</span>
                      <span>•</span>
                      <span>{trial.condition}</span>
                      <span>•</span>
                      <span className={trial.status === 'Recruiting' ? 'text-success' : 'text-primary'}>
                        {trial.status}
                      </span>
                    </div>
                  </div>
                  
                  {/* Match Score */}
                  <div className="text-right ml-6">
                    <div className="mb-2">
                      <p className="text-4xl font-bold text-primaryText">{result.matchScore}%</p>
                      <p className="text-xs text-mutedText mt-1">Overall Match</p>
                    </div>
                    <div className="w-32 h-2 bg-secondary rounded-full overflow-hidden">
                      <div 
                        className={`h-full bg-${getMatchScoreColor(result.matchScore)}`}
                        style={{ width: `${result.matchScore}%` }}
                      />
                    </div>
                    <p className="text-xs text-mutedText mt-2">
                      {result.criteriaSatisfied}/{result.totalCriteria} criteria satisfied
                    </p>
                  </div>
                </div>
              </div>

              {/* Criteria Summary */}
              <div className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h4 className="font-medium text-primaryText">Eligibility Criteria</h4>
                  <Link
                    to={`/trials/${trial.id}`}
                    className="text-sm text-primary hover:text-blue-400 transition-colors"
                  >
                    View Details
                  </Link>
                </div>
                
                <div className="space-y-3">
                  {result.criteria.slice(0, 3).map((criterion, index) => (
                    <div key={index} className="flex items-start gap-3 p-3 bg-secondary rounded-lg">
                      <div className="flex-shrink-0 mt-0.5">
                        {criterion.result === 'PASS' && (
                          <div className="w-5 h-5 rounded-full bg-success/20 flex items-center justify-center">
                            <span className="text-success text-xs">✓</span>
                          </div>
                        )}
                        {criterion.result === 'FAIL' && (
                          <div className="w-5 h-5 rounded-full bg-danger/20 flex items-center justify-center">
                            <span className="text-danger text-xs">✕</span>
                          </div>
                        )}
                        {criterion.result === 'UNKNOWN' && (
                          <div className="w-5 h-5 rounded-full bg-warning/20 flex items-center justify-center">
                            <span className="text-warning text-xs">?</span>
                          </div>
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-primaryText font-medium">{criterion.criterion}</p>
                        <p className="text-xs text-secondaryText mt-1">{criterion.explanation}</p>
                      </div>
                    </div>
                  ))}
                  
                  {result.criteria.length > 3 && (
                    <p className="text-sm text-mutedText text-center">
                      +{result.criteria.length - 3} more criteria
                    </p>
                  )}
                </div>
              </div>

              {/* Footer */}
              <div className="px-6 py-4 bg-secondary border-t border-border flex justify-between items-center">
                <p className="text-xs text-mutedText">
                  <strong>Research matching score</strong> — not a clinical recommendation.
                </p>
                <Link
                  to={`/trials/${trial.id}`}
                  className="px-4 py-2 bg-primary hover:bg-blue-600 text-white text-sm rounded-lg transition-colors"
                >
                  View Full Details
                </Link>
              </div>
            </div>
          );
        })}
      </div>

      {sortedResults.length === 0 && (
        <div className="text-center py-12">
          <p className="text-mutedText">No matching results found for the selected filter.</p>
        </div>
      )}

      {/* Disclaimer */}
      <div className="mt-8 p-4 bg-warning/10 border border-warning rounded-lg">
        <p className="text-sm text-warning">
          <strong>Research Prototype:</strong> Results are generated for research and evaluation purposes and should not be used as a substitute for clinical judgment.
        </p>
      </div>
    </div>
  );
};

export default Results;
