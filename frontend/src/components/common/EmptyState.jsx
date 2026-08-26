import React from 'react';
import { Inbox } from 'lucide-react';

const EmptyState = ({ 
  icon: Icon = Inbox, 
  title = 'No data found', 
  message = 'There are no items to display at this time.',
  action = null 
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-mutedText" />
      </div>
      <h3 className="text-lg font-medium text-primaryText mb-2">{title}</h3>
      <p className="text-mutedText mb-6 max-w-md">{message}</p>
      {action && <div>{action}</div>}
    </div>
  );
};

export default EmptyState;