import React, { useState, useEffect } from 'react';
import { getReports } from '../services/mockApi';

const Reports = () => {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    getReports().then(setReports);
  }, []);

  if (!reports) {
    return (
      <div className="text-center py-12">
        <p className="text-mutedText">Loading reports...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Total Analyses</p>
          <p className="text-3xl font-bold text-primaryText">{reports.totalAnalyses}</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Average Match Score</p>
          <p className="text-3xl font-bold text-primaryText">{reports.averageMatchScore}%</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Eligible Rate</p>
          <p className="text-3xl font-bold text-success">{reports.eligibleRate}%</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-mutedText mb-2">Unknown Rate</p>
          <p className="text-3xl font-bold text-warning">{reports.unknownRate}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Eligibility Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-primaryText mb-4">Eligibility Distribution</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-secondaryText">Eligible</span>
                <span className="text-primaryText">{reports.eligibilityDistribution.eligible}</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-success h-2 rounded-full" 
                  style={{ width: `${(reports.eligibilityDistribution.eligible / 97) * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-secondaryText">Uncertain</span>
                <span className="text-primaryText">{reports.eligibilityDistribution.uncertain}</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-warning h-2 rounded-full" 
                  style={{ width: `${(reports.eligibilityDistribution.uncertain / 97) * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-secondaryText">Not Eligible</span>
                <span className="text-primaryText">{reports.eligibilityDistribution.notEligible}</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div 
                  className="bg-danger h-2 rounded-full" 
                  style={{ width: `${(reports.eligibilityDistribution.notEligible / 97) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Matching Performance */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-primaryText mb-4">Matching Performance</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-secondary p-4 rounded-lg">
              <p className="text-sm text-mutedText mb-1">Precision</p>
              <p className="text-2xl font-bold text-primaryText">{(reports.matchingPerformance.precision * 100).toFixed(0)}%</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <p className="text-sm text-mutedText mb-1">Recall</p>
              <p className="text-2xl font-bold text-primaryText">{(reports.matchingPerformance.recall * 100).toFixed(0)}%</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <p className="text-sm text-mutedText mb-1">F1 Score</p>
              <p className="text-2xl font-bold text-primaryText">{(reports.matchingPerformance.f1Score * 100).toFixed(0)}%</p>
            </div>
            <div className="bg-secondary p-4 rounded-lg">
              <p className="text-sm text-mutedText mb-1">Accuracy</p>
              <p className="text-2xl font-bold text-primaryText">{(reports.matchingPerformance.accuracy * 100).toFixed(0)}%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Segmentation Metrics */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-primaryText mb-4">Segmentation Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Dice Score</p>
            <p className="text-2xl font-bold text-cyan">{reports.segmentationMetrics.diceScore.toFixed(2)}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">IoU</p>
            <p className="text-2xl font-bold text-cyan">{reports.segmentationMetrics.iou.toFixed(2)}</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Precision</p>
            <p className="text-2xl font-bold text-cyan">{(reports.segmentationMetrics.precision * 100).toFixed(0)}%</p>
          </div>
          <div className="bg-secondary p-4 rounded-lg">
            <p className="text-sm text-mutedText mb-1">Recall</p>
            <p className="text-2xl font-bold text-cyan">{(reports.segmentationMetrics.recall * 100).toFixed(0)}%</p>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="mt-8 p-4 bg-warning/10 border border-warning rounded-lg">
        <p className="text-sm text-warning">
          <strong>Research Prototype:</strong> Results are generated for research and evaluation purposes and should not be used as a substitute for clinical judgment.
        </p>
      </div>
    </div>
  );
};

export default Reports;