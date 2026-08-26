import React from 'react';

const PageContainer = ({ children, title, subtitle }) => {
  return (
    <main className="flex-1 ml-64 pt-16 min-h-screen bg-background">
      <div className="p-6 md:p-8">
        {title && (
          <div className="mb-6">
            <h1 className="text-2xl font-semibold text-primaryText">{title}</h1>
            {subtitle && (
              <p className="text-mutedText mt-1">{subtitle}</p>
            )}
          </div>
        )}
        {children}
      </div>
    </main>
  );
};

export default PageContainer;