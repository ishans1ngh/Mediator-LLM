import React from 'react';

const PageContainer = ({ children, title, subtitle }) => {
  return (
    <main className="min-w-0 flex-1 bg-background">
      <div className="px-4 py-6 md:px-8 md:py-7">
        {title && (
          <div className="mb-6">
            <h1 className="text-[28px] font-semibold leading-8 text-primaryText">{title}</h1>
            {subtitle && (
              <p className="mt-1.5 text-sm text-secondaryText">{subtitle}</p>
            )}
          </div>
        )}
        {children}
      </div>
    </main>
  );
};

export default PageContainer;
