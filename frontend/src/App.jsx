import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import MapContainer from './components/MapContainer';
import RiskCard from './components/RiskCard';
import ReportModal from './components/ReportModal';
import RiskAssessmentDrawer from './components/RiskAssessmentDrawer';
import {
  ShieldAlert,
  AlertTriangle,
  Search,
  Filter,
  Layers,
  Activity,
  History,
  AlertCircle,
  FileText,
  MapPin,
  CheckCircle,
  TrendingUp,
  Award,
} from 'lucide-react';

export default function App() {
  const [summary, setSummary] = useState(null);
  const [locations, setLocations] = useState([]);
  const [historical, setHistorical] = useState([]);
  const [reports, setReports] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedLocation, setSelectedLocation] = useState(null);
  const [activeRiskFilter, setActiveRiskFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('locations'); // locations | alerts | reports | historical
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [resSummary, resLocations, resHistorical, resReports] = await Promise.all([
        axios.get('/api/dashboard/summary'),
        axios.get('/api/risk/locations'),
        axios.get('/api/historical-landslides'),
        axios.get('/api/reports'),
      ]);

      setSummary(resSummary.data);
      setLocations(resLocations.data);
      setHistorical(resHistorical.data);
      setReports(resReports.data);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Unable to connect to FastAPI backend service. Ensure server is running on http://127.0.0.1:8000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredLocations = locations.filter((loc) => {
    const matchesFilter = activeRiskFilter === 'ALL' || loc.risk_level === activeRiskFilter;
    const matchesSearch =
      loc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      loc.state.toLowerCase().includes(searchQuery.toLowerCase()) ||
      loc.district.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const criticalCount = locations.filter((l) => l.risk_level === 'CRITICAL').length;
  const highCount = locations.filter((l) => l.risk_level === 'HIGH').length;
  const highestRiskLoc = locations.length > 0 ? locations[0] : null;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-slate-950">
      {/* Top Navigation */}
      <Navbar
        summary={summary}
        onRefresh={fetchData}
        onOpenReportModal={() => setIsReportModalOpen(true)}
        loading={loading}
      />

      {/* Safety disclosure: this repository currently uses illustrative demo data */}
      <div
        role="status"
        className="border-b border-amber-400/30 bg-amber-500/10 px-4 py-2.5 text-center text-xs text-amber-200"
      >
        <span className="font-extrabold tracking-wide">DEMO MODE — </span>
        Illustrative risk scores, rainfall values, alerts, reports, and historical records only. Not live warnings or verified observations; do not use for real-world safety decisions.
      </div>

      {/* Connection Warning Banner if offline */}
      {error && (
        <div className="bg-red-500/10 border-b border-red-500/30 text-red-400 px-4 py-2.5 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <span>{error}</span>
          </div>
          <button
            onClick={fetchData}
            className="px-2.5 py-1 bg-red-500/20 hover:bg-red-500/30 rounded font-semibold text-[11px]"
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Main Dashboard Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-3 lg:p-5 flex flex-col gap-4">
        {/* Risk Intelligence Summary Bar */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex items-center gap-3 backdrop-blur-md">
            <div className="p-2 bg-red-500/10 text-red-400 border border-red-500/30 rounded-lg">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Critical Sectors</span>
              <div className="text-lg font-black text-red-400">{criticalCount} Zones</div>
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex items-center gap-3 backdrop-blur-md">
            <div className="p-2 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded-lg">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">High Risk Zones</span>
              <div className="text-lg font-black text-amber-400">{highCount} Zones</div>
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex items-center gap-3 backdrop-blur-md">
            <div className="p-2 bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded-lg">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Active Warnings</span>
              <div className="text-lg font-black text-cyan-400">{summary?.active_alerts?.length || 0} Alerts</div>
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex items-center gap-3 backdrop-blur-md">
            <div className="p-2 bg-purple-500/10 text-purple-400 border border-purple-500/30 rounded-lg">
              <TrendingUp className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Highest Threat Zone</span>
              <div className="text-xs font-bold text-purple-300 truncate max-w-[140px]">
                {highestRiskLoc ? highestRiskLoc.name : 'N/A'}
              </div>
            </div>
          </div>
        </section>

        {/* Core Layout: Sidebar + GIS Map + Bottom Tabs */}
        <div className="flex-1 flex flex-col lg:flex-row gap-4 min-h-[550px]">
          {/* Left Sidebar: Controls & Monitored Risk Locations List */}
          <aside className="w-full lg:w-96 flex flex-col bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-md shadow-xl">
            {/* Sidebar Header & Filters */}
            <div className="p-3.5 border-b border-slate-800/80 bg-slate-950/40 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-cyan-400" />
                  <h2 className="font-bold text-sm text-white">Monitored Risk Zones</h2>
                </div>
                <span className="text-[11px] font-semibold text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded-full border border-slate-700">
                  {filteredLocations.length} locations
                </span>
              </div>

              {/* Search Input */}
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search state, corridor, or district..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition"
                />
              </div>

              {/* Risk Level Filter Chips */}
              <div className="flex items-center gap-1 overflow-x-auto pb-1 no-scrollbar text-[11px]">
                {['ALL', 'CRITICAL', 'HIGH', 'MODERATE', 'LOW'].map((filter) => (
                  <button
                    key={filter}
                    onClick={() => setActiveRiskFilter(filter)}
                    className={`px-2.5 py-1 rounded-lg border font-semibold transition-all whitespace-nowrap ${
                      activeRiskFilter === filter
                        ? filter === 'CRITICAL'
                          ? 'bg-red-500/20 border-red-500/60 text-red-400'
                          : filter === 'HIGH'
                          ? 'bg-amber-500/20 border-amber-500/60 text-amber-400'
                          : filter === 'MODERATE'
                          ? 'bg-yellow-500/20 border-yellow-500/60 text-yellow-400'
                          : filter === 'LOW'
                          ? 'bg-emerald-500/20 border-emerald-500/60 text-emerald-400'
                          : 'bg-cyan-500/20 border-cyan-500/60 text-cyan-300'
                        : 'bg-slate-950 border-slate-800 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    {filter}
                  </button>
                ))}
              </div>
            </div>

            {/* Locations Scroll List */}
            <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
              {loading ? (
                <div className="py-12 text-center text-xs text-slate-500">
                  Loading monitored risk locations...
                </div>
              ) : filteredLocations.length === 0 ? (
                <div className="py-12 text-center text-xs text-slate-500 space-y-1">
                  <AlertCircle className="w-6 h-6 mx-auto text-slate-600 mb-2" />
                  <p>No risk locations match query.</p>
                </div>
              ) : (
                filteredLocations.map((location) => (
                  <RiskCard
                    key={location.id}
                    location={location}
                    isSelected={selectedLocation?.id === location.id}
                    onClick={() => setSelectedLocation(location)}
                  />
                ))
              )}
            </div>
          </aside>

          {/* Right Panel: GIS Map & Data Tabs */}
          <section className="flex-1 flex flex-col gap-3 min-h-[480px]">
            {/* Top Half: Leaflet GIS Map */}
            <div className="flex-1 relative min-h-[360px]">
              <MapContainer
                locations={locations}
                historical={historical}
                reports={reports}
                selectedLocation={selectedLocation}
                activeRiskFilter={activeRiskFilter}
                onSelectLocation={setSelectedLocation}
              />
            </div>

            {/* Bottom Half: Interactive Data Tabs */}
            <div className="h-44 bg-slate-900/70 border border-slate-800 rounded-2xl flex flex-col overflow-hidden backdrop-blur-md">
              {/* Tab Navigation Headers */}
              <div className="flex items-center gap-1 border-b border-slate-800 bg-slate-950/40 px-3 pt-2 text-xs">
                <button
                  onClick={() => setActiveTab('alerts')}
                  className={`flex items-center gap-1.5 px-3 py-2 border-b-2 font-semibold transition ${
                    activeTab === 'alerts'
                      ? 'border-red-500 text-red-400 bg-red-500/5'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>Active Warnings ({summary?.active_alerts?.length || 0})</span>
                </button>

                <button
                  onClick={() => setActiveTab('reports')}
                  className={`flex items-center gap-1.5 px-3 py-2 border-b-2 font-semibold transition ${
                    activeTab === 'reports'
                      ? 'border-cyan-500 text-cyan-400 bg-cyan-500/5'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <AlertCircle className="w-3.5 h-3.5" />
                  <span>Field Reports ({reports.length})</span>
                </button>

                <button
                  onClick={() => setActiveTab('historical')}
                  className={`flex items-center gap-1.5 px-3 py-2 border-b-2 font-semibold transition ${
                    activeTab === 'historical'
                      ? 'border-purple-500 text-purple-400 bg-purple-500/5'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <History className="w-3.5 h-3.5" />
                  <span>Historical Events ({historical.length})</span>
                </button>
              </div>

              {/* Tab Body Content */}
              <div className="flex-1 overflow-y-auto p-3 text-xs">
                {activeTab === 'alerts' && (
                  <div className="space-y-2">
                    {summary?.active_alerts?.length > 0 ? (
                      summary.active_alerts.map((alert) => (
                        <div
                          key={alert.id}
                          className="p-2.5 bg-slate-950/60 border border-slate-800 rounded-xl flex items-start justify-between gap-2"
                        >
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-slate-200">{alert.location_name}</span>
                              <span className="text-[10px] bg-red-500/20 text-red-400 border border-red-500/30 px-1.5 py-0.2 rounded">
                                {alert.risk_level}
                              </span>
                            </div>
                            <p className="text-slate-400 text-[11px] mt-0.5">{alert.message}</p>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-slate-500 py-4 text-center">No active alerts recorded.</div>
                    )}
                  </div>
                )}

                {activeTab === 'reports' && (
                  <div className="space-y-2">
                    {reports.length > 0 ? (
                      reports.map((rep) => (
                        <div
                          key={rep.id}
                          className="p-2.5 bg-slate-950/60 border border-slate-800 rounded-xl flex items-start justify-between gap-2"
                        >
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-slate-200">{rep.location_name}</span>
                              <span className="text-[10px] text-cyan-400 bg-cyan-500/10 border border-cyan-500/30 px-1.5 py-0.2 rounded">
                                Severity: {rep.severity}
                              </span>
                            </div>
                            <p className="text-slate-300 text-[11px] mt-0.5">{rep.description}</p>
                          </div>
                          <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-1 rounded">
                            Priority: {rep.priority_level}
                          </span>
                        </div>
                      ))
                    ) : (
                      <div className="text-slate-500 py-4 text-center">No citizen field reports yet.</div>
                    )}
                  </div>
                )}

                {activeTab === 'historical' && (
                  <div className="space-y-2">
                    {historical.length > 0 ? (
                      historical.map((ev) => (
                        <div
                          key={ev.id}
                          className="p-2.5 bg-slate-950/60 border border-slate-800 rounded-xl flex items-start justify-between gap-2"
                        >
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-purple-300">{ev.location_name}</span>
                              <span className="text-[10px] text-slate-400 bg-purple-500/10 border border-purple-500/30 px-1.5 py-0.2 rounded">
                                {ev.event_date}
                              </span>
                            </div>
                            <p className="text-slate-300 text-[11px] mt-0.5">{ev.damage_summary}</p>
                          </div>
                          <span className="text-[10px] text-slate-400">{ev.data_source}</span>
                        </div>
                      ))
                    ) : (
                      <div className="text-slate-500 py-4 text-center">No historical records available.</div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Explainability Risk Assessment Drawer */}
      {selectedLocation && (
        <RiskAssessmentDrawer
          location={selectedLocation}
          onClose={() => setSelectedLocation(null)}
        />
      )}

      {/* Citizen Hazard Report Modal */}
      <ReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        onReportSubmitted={fetchData}
      />
    </div>
  );
}
