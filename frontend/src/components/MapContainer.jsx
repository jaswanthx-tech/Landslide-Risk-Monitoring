import React, { useEffect, useState } from 'react';
import { MapContainer as LeafletMap, TileLayer, Marker, Popup, Tooltip, LayersControl, LayerGroup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { AlertTriangle, CloudRain, Mountain, Compass, ShieldAlert, Layers, MapPin, Activity, History, AlertCircle } from 'lucide-react';

// Create custom SVG Leaflet Marker Icons
const createCustomIcon = (color, isCritical = false) => {
  const pulseHtml = isCritical ? `<div class="absolute -top-1 -left-1 w-8 h-8 rounded-full bg-red-500/40 animate-ping"></div>` : '';
  const svgHtml = `
    <div class="relative flex items-center justify-center">
      ${pulseHtml}
      <div class="w-6 h-6 rounded-full flex items-center justify-center shadow-lg border-2 border-slate-950" style="background-color: ${color}">
        <div class="w-2 h-2 rounded-full bg-slate-950"></div>
      </div>
    </div>
  `;
  return L.divIcon({
    html: svgHtml,
    className: 'custom-leaflet-marker',
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12],
  });
};

const riskIcons = {
  CRITICAL: createCustomIcon('#ef4444', true),
  HIGH: createCustomIcon('#f97316'),
  MODERATE: createCustomIcon('#eab308'),
  LOW: createCustomIcon('#22c55e'),
};

const historicalIcon = createCustomIcon('#a855f7');
const reportIcon = createCustomIcon('#f43f5e');

// Helper to center map view on selected location & invalidate container size
function ChangeMapView({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    if (center) {
      map.flyTo(center, zoom, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

export default function MapContainer({
  locations = [],
  historical = [],
  reports = [],
  selectedLocation = null,
  activeRiskFilter = 'ALL',
  onSelectLocation = () => {},
}) {
  // Default map view centered on North-East India
  const defaultCenter = [26.15, 92.5];
  const defaultZoom = 7;

  // Filter locations by risk level tab selection
  const filteredLocations = locations.filter((loc) => {
    if (activeRiskFilter === 'ALL') return true;
    return loc.risk_level === activeRiskFilter;
  });

  const getRiskBadgeColor = (riskLevel) => {
    switch (riskLevel) {
      case 'CRITICAL':
        return 'bg-red-500/20 text-red-400 border-red-500/40';
      case 'HIGH':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'MODERATE':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40';
      case 'LOW':
      default:
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
    }
  };

  const mapCenter = selectedLocation
    ? [selectedLocation.latitude, selectedLocation.longitude]
    : defaultCenter;
  const mapZoom = selectedLocation ? 10 : defaultZoom;

  return (
    <div className="relative w-full h-full rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950">
      <LeafletMap
        center={defaultCenter}
        zoom={defaultZoom}
        zoomControl={false}
        className="w-full h-full"
      >
        <ChangeMapView center={mapCenter} zoom={mapZoom} />

        {/* Base Map Tile Layers (No API Key Required) */}
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="Dark Canvas (Esri GIS)">
            <TileLayer
              attribution='&copy; <a href="https://www.esri.com/">Esri</a> &copy; <a href="https://openstreetmap.org">OSM</a>'
              url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Satellite Imagery (Esri)">
            <TileLayer
              attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Standard OpenStreetMap">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
          </LayersControl.BaseLayer>

          {/* Overlay Layer Groups */}
          <LayersControl.Overlay checked name="Demo Risk Scores (/api/risk/locations)">
            <LayerGroup>
              {filteredLocations.map((loc) => (
                <Marker
                  key={`loc-${loc.id}`}
                  position={[loc.latitude, loc.longitude]}
                  icon={riskIcons[loc.risk_level] || riskIcons.LOW}
                  eventHandlers={{
                    click: () => onSelectLocation(loc),
                  }}
                >
                  <Tooltip direction="top" offset={[0, -10]} opacity={0.95} permanent={false}>
                    <div className="flex items-center gap-1.5 font-semibold text-xs text-slate-100">
                      <span>{loc.name}</span>
                      <span className="text-[10px] text-cyan-400 font-bold">({loc.risk_level})</span>
                    </div>
                  </Tooltip>
                  <Popup>
                    <div className="p-1 max-w-xs space-y-2 text-xs">
                      <div className="flex items-center justify-between gap-2 border-b border-slate-700/60 pb-1.5">
                        <span className="font-bold text-sm text-slate-100">{loc.name}</span>
                        <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full border ${getRiskBadgeColor(loc.risk_level)}`}>
                          {loc.risk_level}
                        </span>
                      </div>

                      <div className="text-slate-300 text-[11px] leading-tight">
                        <strong>State / District:</strong> {loc.state} ({loc.district})
                      </div>

                      <div className="grid grid-cols-2 gap-1.5 bg-slate-900/80 p-2 rounded-lg border border-slate-800 text-[11px]">
                        <div>
                          <span className="text-slate-400">Elevation:</span> <span className="font-medium text-cyan-300">{loc.elevation_m} m</span>
                        </div>
                        <div>
                          <span className="text-slate-400">Slope:</span> <span className="font-medium text-amber-300">{loc.slope_deg}°</span>
                        </div>
                        <div>
                          <span className="text-slate-400">Rain 24h:</span> <span className="font-medium text-blue-300">{loc.rainfall_1d_mm} mm</span>
                        </div>
                        <div>
                          <span className="text-slate-400">Rain 7d:</span> <span className="font-medium text-blue-300">{loc.rainfall_7d_mm} mm</span>
                        </div>
                      </div>

                      {/* Risk Score Bar */}
                      <div>
                        <div className="flex justify-between text-[10px] text-slate-400 mb-1">
                          <span>Demo Risk Index (heuristic)</span>
                          <span className="font-bold text-slate-200">{Math.round(loc.risk_score * 100)} / 100</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              loc.risk_level === 'CRITICAL'
                                ? 'bg-red-500'
                                : loc.risk_level === 'HIGH'
                                ? 'bg-amber-500'
                                : loc.risk_level === 'MODERATE'
                                ? 'bg-yellow-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{ width: `${Math.round(loc.risk_score * 100)}%` }}
                          ></div>
                        </div>
                      </div>

                      {loc.contributing_factors && (
                        <div className="bg-slate-900/50 p-2 rounded border border-slate-800 text-[10px] text-slate-300">
                          <strong className="text-slate-400">Triggers:</strong> {loc.contributing_factors}
                        </div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              ))}
            </LayerGroup>
          </LayersControl.Overlay>

          <LayersControl.Overlay name="Demo Historical Records (/api/historical-landslides)">
            <LayerGroup>
              {historical.map((ev) => (
                <Marker
                  key={`hist-${ev.id}`}
                  position={[ev.latitude, ev.longitude]}
                  icon={historicalIcon}
                >
                  <Popup>
                    <div className="p-1 space-y-1.5 text-xs">
                      <div className="font-bold text-purple-300 border-b border-purple-900/50 pb-1 flex items-center gap-1">
                        <History className="w-3.5 h-3.5" />
                        <span>{ev.is_demo_data ? "Demo Historical Record — Unverified" : "Historical Record — Verify Source"}</span>
                      </div>
                      <div className="font-semibold text-slate-100">{ev.location_name}</div>
                      <div className="text-slate-400 text-[11px]">
                        Date: {ev.event_date} | Trigger: {ev.trigger_type}
                      </div>
                      {ev.damage_summary && (
                        <div className="text-[11px] text-slate-300 bg-slate-900 p-1.5 rounded">
                          {ev.damage_summary}
                        </div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              ))}
            </LayerGroup>
          </LayersControl.Overlay>

          <LayersControl.Overlay name="Field Incident Reports (demo records marked)">
            <LayerGroup>
              {reports.map((rep) => (
                <Marker
                  key={`rep-${rep.id}`}
                  position={[rep.latitude, rep.longitude]}
                  icon={reportIcon}
                >
                  <Popup>
                    <div className="p-1 space-y-1.5 text-xs">
                      <div className="font-bold text-rose-400 border-b border-rose-900/50 pb-1 flex items-center gap-1">
                        <AlertCircle className="w-3.5 h-3.5" />
                        <span>{rep.is_demo_data ? "Demo Field Report — Unverified" : `Field Report (${rep.severity})`}</span>
                      </div>
                      <div className="font-semibold text-slate-100">{rep.location_name}</div>
                      <div className="text-slate-300 text-[11px]">{rep.description}</div>
                      <div className="text-[10px] text-slate-400">
                        Road Blocked: <strong className={rep.road_blocked ? 'text-red-400' : 'text-emerald-400'}>{rep.road_blocked ? 'YES' : 'NO'}</strong> | Priority: {rep.priority_level}
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))}
            </LayerGroup>
          </LayersControl.Overlay>
        </LayersControl>
      </LeafletMap>

      {/* Map Header Overlay Banner */}
      <div className="absolute top-3 left-3 z-[400] bg-slate-900/90 backdrop-blur-md border border-slate-800 px-3 py-2 rounded-xl shadow-lg flex items-center gap-3">
        <MapPin className="w-4 h-4 text-cyan-400" />
        <div className="text-xs">
          <span className="font-semibold text-slate-200">North-East India GIS Prototype</span>
          <span className="text-slate-400 ml-2">({filteredLocations.length} locations visible)</span>
        </div>
      </div>
    </div>
  );
}
