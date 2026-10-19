import React from 'react';
import { ShieldAlert, RefreshCw, PlusCircle, Radio, Activity, Info } from 'lucide-react';

export default function Navbar({ summary, onRefresh, onOpenReportModal, loading }) {
  const overallStatus = summary?.regional_summary?.overall_status || 'LOADING...';

  const getStatusBadge = (status) => {
    if (status.includes('CRITICAL')) {
      return 'bg-red-500/20 text-red-400 border-red-500/40 animate-pulse';
    } else if (status.includes('HIGH')) {
      return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
    } else if (status.includes('MODERATE')) {
      return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40';
    }
    return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
  };

  return (
    <header className="bg-slate-900/90 border-b border-slate-800 backdrop-blur-md sticky top-0 z-[1000] px-4 lg:px-6 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Left: Brand Identity */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg shadow-cyan-500/20">
              <ShieldAlert className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-extrabold text-lg text-white tracking-tight">
                  NER Landslide Sentinel
                </h1>
                <span className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                  SIH26001
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Landslide Risk Prototype & GIS Monitoring — North-East India
              </p>
            </div>
          </div>

          {/* Mobile Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={loading}
            className="md:hidden p-2 bg-slate-800 text-slate-300 rounded-lg hover:bg-slate-700 transition"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Center: Overall Regional Threat Alert Status */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-semibold ${getStatusBadge(overallStatus)}`}>
            <Radio className="w-4 h-4 animate-ping text-current" />
            <span>DEMO STATUS: {overallStatus}</span>
          </div>
          {summary?.regional_summary && (
            <div className="hidden lg:flex items-center gap-3 text-xs text-slate-400 bg-slate-950/60 border border-slate-800/80 px-3 py-1.5 rounded-lg">
              <span className="text-slate-300">
                <strong className="text-red-400">{summary.regional_summary.critical_risk_count}</strong> Demo Critical
              </span>
              <span className="text-slate-600">•</span>
              <span className="text-slate-300">
                <strong className="text-amber-400">{summary.regional_summary.high_risk_count}</strong> Demo High
              </span>
              <span className="text-slate-600">•</span>
              <span className="text-slate-300">
                <strong className="text-cyan-400">{summary.regional_summary.average_regional_rainfall_24h_mm} mm</strong> 24h Rain Avg
              </span>
            </div>
          )}
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2.5 w-full md:w-auto justify-end">
          <button
            onClick={onOpenReportModal}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-semibold rounded-lg shadow-md shadow-red-900/30 transition-all hover:scale-[1.02] active:scale-95"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Report Hazard</span>
          </button>

          <button
            onClick={onRefresh}
            disabled={loading}
            className="hidden md:flex items-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700/60 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>
    </header>
  );
}
