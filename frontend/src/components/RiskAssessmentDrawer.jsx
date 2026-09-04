import React, { useEffect, useState } from 'react';
import { X, ShieldAlert, CloudRain, Mountain, History, Activity, CheckCircle2, AlertTriangle, Layers, Info } from 'lucide-react';
import axios from 'axios';

export default function RiskAssessmentDrawer({ location, onClose }) {
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!location) return;

    const fetchAssessment = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(`/api/risk/assessment/${location.id}`);
        setAssessment(res.data);
      } catch (err) {
        console.error('Error fetching risk assessment:', err);
        setError('Failed to fetch detailed risk explainability data.');
      } finally {
        setLoading(false);
      }
    };

    fetchAssessment();
  }, [location]);

  if (!location) return null;

  const getRiskBadgeColor = (level) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-500/20 text-red-400 border-red-500/40 animate-pulse';
      case 'HIGH':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'MODERATE':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40';
      case 'LOW':
      default:
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-[2000] w-full max-w-md bg-slate-900/95 border-l border-slate-800 shadow-2xl backdrop-blur-xl flex flex-col overflow-hidden text-xs transition-all">
      {/* Header */}
      <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-cyan-400" />
          <div>
            <h2 className="font-bold text-sm text-white">{location.name}</h2>
            <p className="text-[11px] text-slate-400">{location.state} • {location.district}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Content Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {loading ? (
          <div className="py-16 text-center text-slate-400 space-y-2">
            <Activity className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
            <p>Computing dynamic multi-factor risk assessment...</p>
          </div>
        ) : error ? (
          <div className="p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl">
            {error}
          </div>
        ) : assessment ? (
          <>
            {/* Overall Risk Score Badge */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                  Calculated Risk Index
                </span>
                <div className="flex items-baseline gap-1 mt-0.5">
                  <span className="text-3xl font-extrabold text-white">
                    {assessment.overall_risk_score}
                  </span>
                  <span className="text-sm font-semibold text-slate-500">/ 100</span>
                </div>
              </div>
              <div className="text-right">
                <span
                  className={`px-3 py-1 text-xs font-bold uppercase rounded-lg border inline-block ${getRiskBadgeColor(
                    assessment.risk_level
                  )}`}
                >
                  {assessment.risk_level}
                </span>
                <p className="text-[10px] text-slate-500 mt-1">Multi-Factor Score</p>
              </div>
            </div>

            {/* Main Contributing Triggers */}
            <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800 space-y-2">
              <h3 className="font-bold text-slate-200 text-xs flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span>Primary Risk Triggers</span>
              </h3>
              <ul className="space-y-1.5 text-[11px] text-slate-300">
                {assessment.main_contributors.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2 bg-slate-900/80 p-2 rounded-lg border border-slate-800">
                    <span className="font-bold text-cyan-400 text-xs">{idx + 1}.</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Visual Factor Contribution Breakdown */}
            <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800 space-y-3">
              <h3 className="font-bold text-slate-200 text-xs flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-cyan-400" />
                <span>Weighted Factor Breakdown (Explainability)</span>
              </h3>

              {/* Rainfall Factor Bar (35%) */}
              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-300 flex items-center gap-1">
                    <CloudRain className="w-3.5 h-3.5 text-blue-400" />
                    Rainfall Trigger (35%)
                  </span>
                  <span className="font-mono font-bold text-blue-300">
                    {assessment.factor_breakdown.rainfall.score} / {assessment.factor_breakdown.rainfall.max} pts
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full"
                    style={{
                      width: `${(assessment.factor_breakdown.rainfall.score / assessment.factor_breakdown.rainfall.max) * 100}%`,
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>24h: {assessment.factor_breakdown.rainfall.raw_24h_mm} mm</span>
                  <span>7d: {assessment.factor_breakdown.rainfall.raw_7d_mm} mm</span>
                </div>
              </div>

              {/* Slope Factor Bar (30%) */}
              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-300 flex items-center gap-1">
                    <Mountain className="w-3.5 h-3.5 text-amber-400" />
                    Terrain Slope (30%)
                  </span>
                  <span className="font-mono font-bold text-amber-300">
                    {assessment.factor_breakdown.slope.score} / {assessment.factor_breakdown.slope.max} pts
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-amber-500 rounded-full"
                    style={{
                      width: `${(assessment.factor_breakdown.slope.score / assessment.factor_breakdown.slope.max) * 100}%`,
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>Gradient: {assessment.factor_breakdown.slope.raw_slope_deg}°</span>
                  <span>Max Scale: 45°</span>
                </div>
              </div>

              {/* Historical Susceptibility Bar (20%) */}
              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-300 flex items-center gap-1">
                    <History className="w-3.5 h-3.5 text-purple-400" />
                    Historical Landslides (20%)
                  </span>
                  <span className="font-mono font-bold text-purple-300">
                    {assessment.factor_breakdown.historical.score} / {assessment.factor_breakdown.historical.max} pts
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple-500 rounded-full"
                    style={{
                      width: `${(assessment.factor_breakdown.historical.score / assessment.factor_breakdown.historical.max) * 100}%`,
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>Nearby Incidents: {assessment.factor_breakdown.historical.nearby_events_count} events</span>
                </div>
              </div>

              {/* Environmental Context Bar (15%) */}
              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-300 flex items-center gap-1">
                    <Activity className="w-3.5 h-3.5 text-emerald-400" />
                    Environmental Context (15%)
                  </span>
                  <span className="font-mono font-bold text-emerald-300">
                    {assessment.factor_breakdown.environment.score} / {assessment.factor_breakdown.environment.max} pts
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full"
                    style={{
                      width: `${(assessment.factor_breakdown.environment.score / assessment.factor_breakdown.environment.max) * 100}%`,
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>Elevation: {assessment.factor_breakdown.environment.elevation_m} m</span>
                  <span>Soil Moisture: {assessment.factor_breakdown.environment.soil_moisture_percent ?? 'N/A'}%</span>
                </div>
              </div>
            </div>

            {/* Data Completeness & Transparency Indicator */}
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-medium text-[11px]">Data Completeness Index</span>
                <span className="font-bold text-cyan-400">
                  {assessment.data_completeness.completeness_percent}%
                </span>
              </div>
              <p className="text-[10px] text-slate-400">
                Available: {assessment.data_completeness.available_factors.join(', ')}
              </p>
              {assessment.data_completeness.missing_factors.length > 0 && (
                <p className="text-[10px] text-amber-400/90">
                  Missing sensor telemetry: {assessment.data_completeness.missing_factors.join(', ')} (weighted without hallucination)
                </p>
              )}
            </div>

            {/* Recommended Safety Action */}
            <div className="p-3.5 bg-cyan-950/40 border border-cyan-500/30 rounded-xl space-y-1.5">
              <div className="flex items-center gap-1.5 font-bold text-cyan-300">
                <Info className="w-4 h-4" />
                <span>Recommended Operational Action</span>
              </div>
              <p className="text-[11px] text-cyan-100/90 leading-relaxed">
                {assessment.recommended_action}
              </p>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}
