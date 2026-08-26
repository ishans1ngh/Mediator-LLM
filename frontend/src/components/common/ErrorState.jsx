import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

const ErrorState = ({ 
  title = 'Something went wrong', 
  message = 'An error occurred while loading the data. Please try again.',
  onRetry = null 
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-danger/10 rounded-full flex items-center justify-center mb-4">
        <AlertCircle className="w-8 h-8 text-danger" />
      </div>
      <h3 className="text-lg font-medium text-primaryText mb-2">{title}</h3>
      <p className="text-mutedText mb-6 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorState;