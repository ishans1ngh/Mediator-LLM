import React from 'react';
import { User, Palette, Bell, Cpu, Database } from 'lucide-react';

const Settings = () => {
  return (
    <div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Navigation */}
        <div className="card p-4">
          <nav className="space-y-1">
            <button className="w-full flex items-center gap-3 px-4 py-3 bg-primary text-white rounded-lg">
              <User className="w-5 h-5" />
              Profile
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 text-secondaryText hover:bg-secondary rounded-lg transition-colors">
              <Palette className="w-5 h-5" />
              Appearance
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 text-secondaryText hover:bg-secondary rounded-lg transition-colors">
              <Bell className="w-5 h-5" />
              Notifications
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 text-secondaryText hover:bg-secondary rounded-lg transition-colors">
              <Cpu className="w-5 h-5" />
              AI Configuration
            </button>
            <button className="w-full flex items-center gap-3 px-4 py-3 text-secondaryText hover:bg-secondary rounded-lg transition-colors">
              <Database className="w-5 h-5" />
              Data Preferences
            </button>
          </nav>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Profile Section */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-primaryText mb-4">Profile</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-mutedText mb-2">Name</label>
                <input
                  type="text"
                  defaultValue="Researcher"
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Email</label>
                <input
                  type="email"
                  defaultValue="researcher@institution.edu"
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm text-mutedText mb-2">Institution</label>
                <input
                  type="text"
                  defaultValue="Medical Research Center"
                  className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-primaryText focus:outline-none focus:border-primary"
                />
              </div>
            </div>
          </div>

          {/* AI Configuration */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-primaryText mb-4">AI Configuration</h3>
            <p className="text-sm text-mutedText mb-4">Read-only prototype configuration</p>
            
            <div className="space-y-4">
              <div className="bg-secondary p-4 rounded-lg">
                <p className="text-sm text-mutedText mb-1">Patient Reader Agent</p>
                <p className="text-primaryText font-medium">Model: GPT-based LLM</p>
              </div>
              <div className="bg-secondary p-4 rounded-lg">
                <p className="text-sm text-mutedText mb-1">Trial Parser Agent</p>
                <p className="text-primaryText font-medium">Model: GPT-based LLM</p>
              </div>
              <div className="bg-secondary p-4 rounded-lg">
                <p className="text-sm text-mutedText mb-1">Mediator Agent</p>
                <p className="text-primaryText font-medium">Model: GPT-based LLM</p>
              </div>
              <div className="bg-secondary p-4 rounded-lg">
                <p className="text-sm text-mutedText mb-1">Imaging Pipeline</p>
                <p className="text-primaryText font-medium">U-Net Segmentation + ResNet-50</p>
              </div>
            </div>
          </div>

          {/* Appearance */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-primaryText mb-4">Appearance</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-primaryText font-medium">Dark Mode</p>
                  <p className="text-sm text-mutedText">Use dark theme</p>
                </div>
                <button className="w-12 h-6 bg-primary rounded-full relative">
                  <span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></span>
                </button>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button className="px-6 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;