import React from 'react';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h3>Clinical Trials</h3>
      </div>
      <div className="sidebar-content">
        <ul>
          <li><a href="/trial/1">Alzheimer's Study</a></li>
          <li><a href="/trial/2">Parkinson's Research</a></li>
          <li><a href="/trial/3">Multiple Sclerosis</a></li>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
