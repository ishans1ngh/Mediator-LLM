import React from 'react';
import { Link } from 'react-router-dom';
import {
  Plus,
  Users,
  ClipboardList,
  CheckCircle,
  AlertCircle,
  Activity,
  TrendingUp,
  TrendingDown,
} from 'lucide-react';
import { mockPatients } from '../data/mockData';

const stats = [
  { title: 'Total Patients', value: 128, icon: Users, trend: '+12% this month', up: true, iconColor: 'text-primary', iconBg: 'bg-primary/10' },
  { title: 'Clinical Trials', value: 64, icon: ClipboardList, trend: '+8% this month', up: true, iconColor: 'text-cyan', iconBg: 'bg-cyan/10' },
  { title: 'AI Analyses', value: 83, icon: Activity, trend: '+6% this month', up: true, iconColor: 'text-info', iconBg: 'bg-info/10' },
  { title: 'Eligible Matches', value: 37, icon: CheckCircle, trend: '+15% this month', up: true, iconColor: 'text-success', iconBg: 'bg-success/10' },
  { title: 'Pending Reviews', value: 8, icon: AlertCircle, trend: '-2% this month', up: false, iconColor: 'text-warning', iconBg: 'bg-warning/10' },
];

const statusStyles = {
  Completed: 'bg-success/10 text-success',
  Processing: 'bg-primary/10 text-primary',
  'Pending Review': 'bg-warning/10 text-warning',
  Failed: 'bg-danger/10 text-danger',
};

const statusDotStyles = {
  Completed: 'bg-success',
  Processing: 'bg-primary',
  'Pending Review': 'bg-warning',
  Failed: 'bg-danger',
};

const matchingOverview = [
  { label: 'Eligible', value: 37, barColor: 'bg-success', textColor: 'text-success' },
  { label: 'Uncertain', value: 18, barColor: 'bg-warning', textColor: 'text-warning' },
  { label: 'Not Eligible', value: 42, barColor: 'bg-danger', textColor: 'text-danger' },
];

const matchingTotal = matchingOverview.reduce((sum, item) => sum + item.value, 0);

const StatusBadge = ({ status }) => (
  <span
    className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
      statusStyles[status] ?? 'bg-danger/10 text-danger'
    }`}
  >
    <span className={`h-1.5 w-1.5 rounded-full ${statusDotStyles[status] ?? 'bg-danger'}`} />
    {status}
  </span>
);

const Dashboard = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <h2 className="text-[28px] font-semibold leading-8 text-primaryText">Dashboard</h2>
          <p className="mt-1.5 text-sm text-secondaryText">
            AI-powered clinical trial matching and eligibility analysis
          </p>
        </div>
        <Link
          to="/patients/new"
          className="flex h-10 flex-shrink-0 items-center gap-2 rounded-lg bg-primary px-4 text-sm font-medium text-white transition-colors duration-150 hover:bg-primary/90"
        >
          <Plus className="h-4 w-4" />
          New Patient
        </Link>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {stats.map((stat) => (
          <div key={stat.title} className="card p-5 transition-colors duration-150 hover:bg-card-hover">
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-secondaryText">{stat.title}</p>
              <div className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg ${stat.iconBg}`}>
                <stat.icon className={`h-4 w-4 ${stat.iconColor}`} strokeWidth={1.75} />
              </div>
            </div>
            <p className="text-[28px] font-semibold leading-8 text-primaryText">{stat.value}</p>
            <p className={`mt-2 flex items-center gap-1 text-xs ${stat.up ? 'text-success' : 'text-danger'}`}>
              {stat.up ? <TrendingUp className="h-3.5 w-3.5" /> : <TrendingDown className="h-3.5 w-3.5" />}
              {stat.trend}
            </p>
          </div>
        ))}
      </div>

      {/* Recent Patients + Matching Overview */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(300px,1fr)]">
        {/* Recent Patients */}
        <div className="card overflow-hidden">
          <div className="flex items-center justify-between border-b border-border p-5">
            <h3 className="text-lg font-semibold text-primaryText">Recent Patients</h3>
            <Link to="/patients" className="text-sm text-primary transition-colors hover:text-primary/80">
              View all →
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-secondary">
                <tr>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Patient ID</th>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Diagnosis</th>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Age</th>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Last Analysis</th>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Matches</th>
                  <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wider text-mutedText">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {mockPatients.slice(0, 5).map((patient) => (
                  <tr key={patient.id} className="transition-colors hover:bg-card-hover">
                    <td className="whitespace-nowrap px-5 py-3.5 text-sm font-medium text-primary">
                      <Link to={`/patients/${patient.id}`} className="transition-colors hover:text-primary/80">
                        {patient.id}
                      </Link>
                    </td>
                    <td className="whitespace-nowrap px-5 py-3.5 text-sm text-secondaryText">{patient.diagnosis}</td>
                    <td className="whitespace-nowrap px-5 py-3.5 text-sm text-secondaryText">{patient.age}</td>
                    <td className="whitespace-nowrap px-5 py-3.5 text-sm text-secondaryText">
                      {patient.lastAnalysis ? new Date(patient.lastAnalysis).toLocaleDateString() : 'Not analyzed'}
                    </td>
                    <td className="whitespace-nowrap px-5 py-3.5 text-sm text-secondaryText">
                      {patient.status === 'Completed' ? '2 matches' : '-'}
                    </td>
                    <td className="whitespace-nowrap px-5 py-3.5">
                      <StatusBadge status={patient.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Matching Overview */}
        <div className="card p-5">
          <h3 className="text-lg font-semibold text-primaryText">Matching Overview</h3>
          <p className="mt-1 text-xs text-mutedText">{matchingTotal} analyses evaluated</p>

          <div className="mt-6 space-y-5">
            {matchingOverview.map((item) => (
              <div key={item.label}>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm text-secondaryText">{item.label}</span>
                  <span className={`text-sm font-semibold ${item.textColor}`}>{item.value}</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-border">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${item.barColor}`}
                    style={{ width: `${Math.round((item.value / matchingTotal) * 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="card p-5">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-primaryText">System Status</h3>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-success/10 px-2.5 py-1 text-xs font-medium text-success">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
            Online
          </span>
        </div>
        <p className="mt-3 text-sm text-primaryText">All systems operational</p>
        <p className="mt-1 text-sm text-mutedText">AI agents running normally.</p>
      </div>
    </div>
  );
};

export default Dashboard;
