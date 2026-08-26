import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  ClipboardList, 
  Activity, 
  FileBarChart, 
  Settings, 
  HelpCircle,
  BrainCircuit
} from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/patients', icon: Users, label: 'Patients' },
    { path: '/trials', icon: ClipboardList, label: 'Clinical Trials' },
    { path: '/analysis', icon: Activity, label: 'Analyses' },
    { path: '/reports', icon: FileBarChart, label: 'Reports' },
  ];

  const systemItems = [
    { path: '/settings', icon: Settings, label: 'Settings' },
    { path: '/help', icon: HelpCircle, label: 'Help' },
  ];

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-secondary border-r border-border flex flex-col z-30">
      {/* Logo */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
            <BrainCircuit className="w-6 h-6 text-white" />
          </div>
          <div className="min-w-0">
            <h1 className="text-lg font-semibold text-primaryText truncate">ClinicalAI</h1>
            <p className="text-xs text-mutedText">Trial Matching</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-6">
        <div className="px-4 mb-6">
          <p className="text-xs font-medium text-mutedText uppercase tracking-wider mb-3 px-3">
            Main
          </p>
          <ul className="space-y-1">
            {navItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary text-white'
                      : 'text-secondaryText hover:bg-card hover:text-primaryText'
                  }`}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  <span className="font-medium truncate">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="px-4">
          <p className="text-xs font-medium text-mutedText uppercase tracking-wider mb-3 px-3">
            System
          </p>
          <ul className="space-y-1">
            {systemItems.map((item) => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary text-white'
                      : 'text-secondaryText hover:bg-card hover:text-primaryText'
                  }`}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  <span className="font-medium truncate">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 bg-cyan rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-sm font-semibold text-white">R</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-primaryText truncate">Researcher</p>
            <p className="text-xs text-success">Online</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;