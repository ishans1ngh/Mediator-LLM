import React from 'react';
import { Bell, Search, User } from 'lucide-react';

const Topbar = ({ title }) => {
  return (
    <header className="fixed top-0 left-64 right-0 h-16 bg-secondary border-b border-border flex items-center justify-between px-6 z-20">
      {/* Page Title */}
      <div className="flex items-center gap-4 min-w-0">
        <h1 className="text-xl font-semibold text-primaryText truncate">{title}</h1>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-4 flex-shrink-0">
        {/* Search */}
        <div className="relative hidden md:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-mutedText" />
          <input
            type="text"
            placeholder="Search patients, trials..."
            className="pl-10 pr-4 py-2 bg-card border border-border rounded-lg text-sm text-primaryText placeholder-mutedText focus:outline-none focus:border-primary w-64"
          />
        </div>

        {/* Notifications */}
        <button className="relative p-2 text-secondaryText hover:text-primaryText transition-colors flex-shrink-0" aria-label="Notifications">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-danger rounded-full"></span>
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-4 border-l border-border flex-shrink-0">
          <div className="w-8 h-8 bg-cyan rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
          <div className="text-sm hidden md:block">
            <p className="font-medium text-primaryText">Researcher</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Topbar;