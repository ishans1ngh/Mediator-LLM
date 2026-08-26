import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter } from 'lucide-react';
import { mockTrials } from '../data/mockData';

const Trials = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [phaseFilter, setPhaseFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');

  const filteredTrials = mockTrials.filter(trial => {
    const matchesSearch = trial.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         trial.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         trial.condition.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPhase = phaseFilter === 'All' || trial.phase === phaseFilter;
    const matchesStatus = statusFilter === 'All' || trial.status === statusFilter;
    
    return matchesSearch && matchesPhase && matchesStatus;
  });

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-primaryText">Clinical Trials</h2>
        <p className="text-mutedText mt-1">Search and explore clinical trials</p>
      </div>

      {/* Search and Filters */}
      <div className="flex gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-mutedText" />
          <input
            type="text"
            placeholder="Search by condition, NCT ID, or trial title..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 card text-sm text-primaryText placeholder-mutedText focus:outline-none focus:border-primary"
          />
        </div>
        
        <select
          value={phaseFilter}
          onChange={(e) => setPhaseFilter(e.target.value)}
          className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary"
        >
          <option value="All">All Phases</option>
          <option value="Phase I">Phase I</option>
          <option value="Phase II">Phase II</option>
          <option value="Phase III">Phase III</option>
        </select>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 card text-primaryText focus:outline-none focus:border-primary"
        >
          <option value="All">All Statuses</option>
          <option value="Recruiting">Recruiting</option>
          <option value="Active">Active</option>
          <option value="Completed">Completed</option>
        </select>
      </div>

      {/* Trial Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTrials.map((trial) => (
          <Link
            key={trial.id}
            to={`/trials/${trial.id}`}
            className="card p-6 hover:border-primary transition-colors cursor-pointer"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <p className="text-xs text-mutedText mb-1">{trial.id}</p>
                <h3 className="font-semibold text-primaryText line-clamp-2">{trial.title}</h3>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                trial.status === 'Recruiting' ? 'bg-success/20 text-success' :
                trial.status === 'Active' ? 'bg-primary/20 text-primary' :
                'bg-mutedText/20 text-mutedText'
              }`}>
                {trial.status}
              </span>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-mutedText">Phase</span>
                <span className="text-primaryText">{trial.phase}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-mutedText">Condition</span>
                <span className="text-primaryText">{trial.condition}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-mutedText">Enrollment</span>
                <span className="text-primaryText">{trial.enrollment}</span>
              </div>
            </div>

            <p className="text-sm text-secondaryText line-clamp-3 mb-4">{trial.description}</p>

            <div className="text-xs text-mutedText">
              <p>{trial.location}</p>
            </div>
          </Link>
        ))}
      </div>

      {filteredTrials.length === 0 && (
        <div className="text-center py-12">
          <p className="text-mutedText">No clinical trials found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Trials;