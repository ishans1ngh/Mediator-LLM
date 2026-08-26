import React from 'react';
import { useLocation } from 'react-router-dom';
import { Bell, Menu, Search, User } from 'lucide-react';

const routeTitles = [
  { pattern: /^\/dashboard/, title: 'Dashboard' },
  { pattern: /^\/patients\/new/, title: 'New Patient' },
  { pattern: /^\/patients\/[^/]+/, title: 'Patient Details' },
  { pattern: /^\/patients/, title: 'Patients' },
  { pattern: /^\/analysis/, title: 'Analysis' },
  { pattern: /^\/results/, title: 'Matching Results' },
  { pattern: /^\/trials\/[^/]+/, title: 'Trial Details' },
  { pattern: /^\/trials/, title: 'Clinical Trials' },
  { pattern: /^\/reports/, title: 'Reports' },
  { pattern: /^\/settings/, title: 'Settings' },
];

const Topbar = ({ onMenuClick }) => {
  const location = useLocation();
  const title = routeTitles.find((r) => r.pattern.test(location.pathname))?.title ?? 'Dashboard';

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b border-border bg-background/80 px-4 backdrop-blur md:px-8">
      {/* Left: mobile menu + page title */}
      <div className="flex min-w-0 items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          aria-label="Open menu"
          className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg border border-border bg-card text-secondaryText transition-colors hover:text-primaryText lg:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>
        <h1 className="truncate text-sm font-medium text-secondaryText">{title}</h1>
      </div>

      {/* Right: search, notifications, profile */}
      <div className="flex flex-shrink-0 items-center gap-3">
        <div className="relative hidden md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-mutedText" />
          <input
            type="text"
            aria-label="Search patients and trials"
            placeholder="Search patients, trials..."
            className="h-10 w-56 rounded-lg border border-border bg-card pl-10 pr-4 text-sm text-primaryText placeholder-mutedText transition-colors focus:border-primary focus:outline-none lg:w-64"
          />
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg border border-border bg-card text-secondaryText transition-colors hover:text-primaryText"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute right-2.5 top-2.5 h-2 w-2 rounded-full bg-danger" />
        </button>

        <div className="flex flex-shrink-0 items-center gap-2.5 border-l border-border pl-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-cyan">
            <User className="h-4 w-4 text-white" />
          </div>
          <p className="hidden text-sm font-medium text-primaryText md:block">Researcher</p>
        </div>
      </div>
    </header>
  );
};

export default Topbar;
