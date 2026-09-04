import React from 'react';
import { AlertTriangle, CloudRain, Mountain, ChevronRight, ShieldAlert } from 'lucide-react';

export default function RiskCard({ location, isSelected, onClick }) {
  const getBadgeStyle = (level) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-500/10 text-red-400 border-red-500/30 ring-1 ring-red-500/20';
      case 'HIGH':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'MODERATE':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
      case 'LOW':
      default:
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    }
  };

  return (
    <div
      onClick={onClick}
      className={`p-3.5 rounded-xl border transition-all duration-200 cursor-pointer ${
        isSelected
          ? 'bg-slate-800/90 border-cyan-500/80 shadow-lg shadow-cyan-500/10 ring-1 ring-cyan-500/50'
          : 'bg-slate-900/60 border-slate-800/80 hover:bg-slate-850 hover:border-slate-700'
      }`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <h3 className="font-semibold text-sm text-slate-100 group-hover:text-cyan-400 transition">
            {location.name}
          </h3>
          <p className="text-xs text-slate-400">
            {location.state} • {location.district}
          </p>
        </div>
        <span
          className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-md border tracking-wider ${getBadgeStyle(
            location.risk_level
          )}`}
        >
          {location.risk_level}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 py-2 px-2.5 bg-slate-950/60 rounded-lg border border-slate-800/60 text-xs mb-2">
        <div className="flex flex-col">
          <span className="text-[10px] text-slate-400">24h Rain</span>
          <span className="font-medium text-cyan-300 flex items-center gap-1">
            <CloudRain className="w-3 h-3 text-cyan-400" />
            {location.rainfall_1d_mm} mm
          </span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-slate-400">Slope</span>
          <span className="font-medium text-amber-300 flex items-center gap-1">
            <Mountain className="w-3 h-3 text-amber-400" />
            {location.slope_deg}°
          </span>
        </div>
        <div className="flex flex-col">
          <span className="text-[10px] text-slate-400">Risk Score</span>
          <span className="font-bold text-slate-100">
            {Math.round(location.risk_score * 100)}%
          </span>
        </div>
      </div>

      {location.contributing_factors && (
        <p className="text-[11px] text-slate-400 line-clamp-1 italic">
          "{location.contributing_factors}"
        </p>
      )}
    </div>
  );
}
