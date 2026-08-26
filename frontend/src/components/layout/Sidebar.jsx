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
  BrainCircuit,
  X,
} from 'lucide-react';

const navItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/patients', icon: Users, label: 'Patients' },
  { path: '/trials', icon: ClipboardList, label: 'Clinical Trials' },
  { path: '/analysis', icon: Activity, label: 'AI Analyses' },
  { path: '/reports', icon: FileBarChart, label: 'Reports' },
];

const systemItems = [
  { path: '/settings', icon: Settings, label: 'Settings' },
  { path: '/help', icon: HelpCircle, label: 'Help' },
];

const NavLink = ({ item, isActive }) => (
  <li>
    <Link
      to={item.path}
      aria-current={isActive ? 'page' : undefined}
      className={`flex h-10 items-center gap-2.5 rounded-lg px-3 text-sm transition-colors duration-150 ${
        isActive
          ? 'bg-primary/10 text-primary font-medium'
          : 'text-secondaryText hover:bg-card hover:text-primaryText'
      }`}
    >
      <item.icon className="h-5 w-5 flex-shrink-0" strokeWidth={1.75} />
      <span className="truncate">{item.label}</span>
    </Link>
  </li>
);

const Sidebar = ({ open = false, onClose }) => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          aria-hidden="true"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-[250px] flex-col border-r border-border bg-secondary transition-transform duration-200 ease-in-out ${
          open ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0`}
      >
        {/* Logo */}
        <div className="flex items-center justify-between border-b border-border px-5 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg bg-primary">
              <BrainCircuit className="h-5 w-5 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="truncate text-[15px] font-semibold leading-tight text-primaryText">TrialMatch AI</h1>
              <p className="text-xs text-mutedText">Research Platform</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close menu"
            className="rounded-lg p-1.5 text-mutedText transition-colors hover:bg-card hover:text-primaryText lg:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4">
          <p className="mb-2 px-3 text-[11px] font-medium uppercase tracking-wider text-mutedText">
            Main
          </p>
          <ul className="flex flex-col gap-1">
            {navItems.map((item) => (
              <NavLink key={item.path} item={item} isActive={isActive(item.path)} />
            ))}
          </ul>

          <p className="mb-2 mt-6 px-3 text-[11px] font-medium uppercase tracking-wider text-mutedText">
            System
          </p>
          <ul className="flex flex-col gap-1">
            {systemItems.map((item) => (
              <NavLink key={item.path} item={item} isActive={isActive(item.path)} />
            ))}
          </ul>
        </nav>

        {/* User Profile */}
        <div className="border-t border-border p-4">
          <div className="flex items-center gap-3 px-2">
            <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-cyan">
              <span className="text-sm font-semibold text-white">R</span>
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-primaryText">Researcher</p>
              <p className="flex items-center gap-1.5 text-xs text-mutedText">
                <span className="h-1.5 w-1.5 rounded-full bg-success" />
                Online
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
