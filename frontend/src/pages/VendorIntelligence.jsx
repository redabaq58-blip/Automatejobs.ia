import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  Cpu, ShieldCheck, AlertTriangle, Radio, Layers, Radar
} from 'lucide-react';
import { useApi } from '@/hooks/useApi';
import {
  getAITools, getVendors,
  getTCOAll, getTCOHiddenMultipliers,
  getFailureRates,
  getTechRadar, getTechAdoptNow
} from '@/lib/api';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatCurrency(val) {
  if (val == null) return '—';
  const n = Number(val);
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(0)}k`;
  return `$${n.toFixed(0)}`;
}

function categoryBadgeClass(cat) {
  const map = {
    RPA: 'bg-violet-100 text-violet-800 border-violet-200',
    'LLM/GPT': 'bg-blue-100 text-blue-800 border-blue-200',
    'Document AI': 'bg-emerald-100 text-emerald-800 border-emerald-200',
    Conversational: 'bg-amber-100 text-amber-800 border-amber-200',
    Analytics: 'bg-orange-100 text-orange-800 border-orange-200',
  };
  return map[cat] ?? 'bg-gray-100 text-gray-700 border-gray-200';
}

function multiplierColor(mult) {
  if (mult > 2.5) return 'text-red-600 font-semibold';
  if (mult >= 1.5) return 'text-amber-600 font-semibold';
  return 'text-emerald-600 font-semibold';
}

function failureRateColor(rate) {
  const r = parseFloat(rate);
  if (r > 30) return 'text-red-600 font-semibold';
  if (r >= 15) return 'text-amber-600 font-semibold';
  return 'text-emerald-600 font-semibold';
}

const TOOL_CATEGORIES = ['All', 'RPA', 'LLM/GPT', 'Document AI', 'Conversational', 'Analytics'];

// ─── Tab 1 – AI Tools ─────────────────────────────────────────────────────────

function AIToolsTab() {
  const [activeFilter, setActiveFilter] = useState('All');
  const { data: tools, loading: toolsLoading, error: toolsError, refetch: refetchTools } =
    useApi(getAITools, []);
  const { data: vendors, loading: vendorsLoading } = useApi(getVendors, []);

  const vendorMap = {};
  if (vendors) vendors.forEach((v) => { vendorMap[v.id ?? v.name] = v; });

  const filtered = tools
    ? tools.filter((t) => activeFilter === 'All' || t.category === activeFilter)
    : [];

  if (toolsLoading || vendorsLoading) return <LoadingCards count={6} className="grid-cols-1 sm:grid-cols-2 lg:grid-cols-3" />;
  if (toolsError) return <ErrorState error={toolsError} onRetry={refetchTools} />;

  return (
    <div className="space-y-5">
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2">
        {TOOL_CATEGORIES.map((cat) => (
          <Button
            key={cat}
            size="sm"
            variant={activeFilter === cat ? 'default' : 'outline'}
            className={
              activeFilter === cat
                ? 'bg-violet-600 hover:bg-violet-700 text-white h-8 text-xs'
                : 'h-8 text-xs text-gray-600 hover:text-violet-600 hover:border-violet-300'
            }
            onClick={() => setActiveFilter(cat)}
          >
            {cat}
          </Button>
        ))}
        <span className="text-xs text-gray-400 self-center ml-1">{filtered.length} tools</span>
      </div>

      {/* Tool grid */}
      {!filtered.length ? (
        <p className="text-sm text-gray-400 py-8 text-center">No tools found for this category.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((tool, i) => (
            <Card key={i} className="bg-white shadow-sm rounded-xl border hover:shadow-md transition-shadow">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <p className="text-base font-bold text-gray-900 truncate">{tool.name}</p>
                    <p className="text-xs text-gray-500 truncate">{tool.vendor ?? '—'}</p>
                  </div>
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border shrink-0 ${categoryBadgeClass(
                      tool.category
                    )}`}
                  >
                    {tool.category ?? 'Tool'}
                  </span>
                </div>

                {tool.description && (
                  <p className="text-xs text-gray-600 line-clamp-2">{tool.description}</p>
                )}

                <div className="flex flex-wrap gap-1.5 pt-1">
                  {tool.pricing && (
                    <Badge variant="outline" className="text-xs font-normal">
                      {tool.pricing}
                    </Badge>
                  )}
                  {tool.gdpr_compliant && (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
                      <ShieldCheck className="h-3 w-3" />
                      GDPR
                    </span>
                  )}
                  {tool.enterprise_ready && (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200">
                      Enterprise Ready
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Tab 2 – TCO Analysis ─────────────────────────────────────────────────────

function TCOTab() {
  const { data: tcoAll, loading: tcoLoading, error: tcoError, refetch: refetchTCO } =
    useApi(getTCOAll, []);
  const { data: multipliers, loading: multLoading } = useApi(getTCOHiddenMultipliers, []);

  const loading = tcoLoading || multLoading;

  if (loading) return <LoadingTable rows={6} cols={5} />;
  if (tcoError) return <ErrorState error={tcoError} onRetry={refetchTCO} />;

  // Build chart data
  const chartData = (tcoAll ?? []).map((row) => ({
    name: row.automation_type ?? row.type ?? '—',
    visible: row.visible_cost ?? 0,
    hidden: row.hidden_cost ?? (row.visible_cost ?? 0) * ((row.hidden_multiplier ?? 1.5) - 1),
  }));

  return (
    <div className="space-y-6">
      {/* Warning banner */}
      <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-4">
        <AlertTriangle className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-semibold text-amber-800">Hidden Cost Warning</p>
          <p className="text-xs text-amber-700 mt-0.5">
            Hidden costs average <strong>1.5–3x</strong> the visible cost. Factor these in before signing any vendor contract.
          </p>
        </div>
      </div>

      {/* Table */}
      {tcoAll?.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-gray-50">
                {['Automation Type', 'Visible Cost ($)', 'Hidden Cost Multiplier', 'TCO 5-Year', 'Risk Level'].map(
                  (h) => (
                    <th
                      key={h}
                      className="text-left px-3 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap"
                    >
                      {h}
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody>
              {tcoAll.map((row, i) => (
                <tr key={i} className="border-b hover:bg-gray-50 transition-colors">
                  <td className="px-3 py-3 font-medium text-gray-900 whitespace-nowrap">
                    {row.automation_type ?? row.type ?? '—'}
                  </td>
                  <td className="px-3 py-3 text-gray-700 whitespace-nowrap">
                    {formatCurrency(row.visible_cost)}
                  </td>
                  <td className={`px-3 py-3 whitespace-nowrap ${multiplierColor(row.hidden_multiplier)}`}>
                    {row.hidden_multiplier != null ? `${row.hidden_multiplier}x` : '—'}
                  </td>
                  <td className="px-3 py-3 font-semibold text-gray-800 whitespace-nowrap">
                    {formatCurrency(row.tco_5_year ?? row.five_year_tco)}
                  </td>
                  <td className="px-3 py-3 whitespace-nowrap">
                    {row.risk_level ? (
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${
                          row.risk_level === 'HIGH' || row.risk_level === 'CRITICAL'
                            ? 'bg-red-100 text-red-800 border-red-200'
                            : row.risk_level === 'MEDIUM'
                            ? 'bg-amber-100 text-amber-800 border-amber-200'
                            : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                        }`}
                      >
                        {row.risk_level}
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Stacked Bar Chart */}
      {chartData.length > 0 && (
        <div>
          <p className="text-sm font-semibold text-gray-700 mb-3">
            Visible vs Hidden Costs by Automation Type
          </p>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={chartData} margin={{ top: 4, right: 12, left: 0, bottom: 40 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 10 }}
                angle={-30}
                textAnchor="end"
                interval={0}
              />
              <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => formatCurrency(v)} width={56} />
              <Tooltip formatter={(v, name) => [formatCurrency(v), name]} />
              <Legend verticalAlign="top" height={28} />
              <Bar dataKey="visible" name="Visible Cost" stackId="a" fill="#7c3aed" radius={[0, 0, 0, 0]} />
              <Bar dataKey="hidden" name="Hidden Cost" stackId="a" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {!tcoAll?.length && (
        <p className="text-sm text-gray-400 py-8 text-center">No TCO data available.</p>
      )}
    </div>
  );
}

// ─── Tab 3 – Failure Rates ────────────────────────────────────────────────────

function FailureRatesTab() {
  const { data, loading, error, refetch } = useApi(getFailureRates, []);

  if (loading) return <LoadingTable rows={6} cols={4} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!data?.length) return <p className="text-sm text-gray-400 py-8 text-center">No failure rate data available.</p>;

  const sorted = [...data].sort((a, b) => (b.failure_rate ?? 0) - (a.failure_rate ?? 0));
  const topWarnings = sorted.slice(0, 3).filter((r) => parseFloat(r.failure_rate) > 15);

  return (
    <div className="space-y-6">
      {/* Warning cards */}
      {topWarnings.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {topWarnings.map((row, i) => (
            <div
              key={i}
              className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3"
            >
              <AlertTriangle className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-red-800">
                  {row.automation_type ?? row.type ?? '—'}
                </p>
                <p className="text-xs text-red-700 mt-0.5">
                  {row.failure_rate != null ? `${row.failure_rate}% failure rate` : 'High failure risk'}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-gray-50">
              {['Automation Type', 'Failure Rate %', 'MTTR (hours)', 'Recommended SLA', 'Risk Level'].map(
                (h) => (
                  <th
                    key={h}
                    className="text-left px-3 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap"
                  >
                    {h}
                  </th>
                )
              )}
            </tr>
          </thead>
          <tbody>
            {sorted.map((row, i) => (
              <tr key={i} className="border-b hover:bg-gray-50 transition-colors">
                <td className="px-3 py-3 font-medium text-gray-900 whitespace-nowrap">
                  {row.automation_type ?? row.type ?? '—'}
                </td>
                <td className={`px-3 py-3 whitespace-nowrap ${failureRateColor(row.failure_rate)}`}>
                  {row.failure_rate != null ? `${row.failure_rate}%` : '—'}
                </td>
                <td className="px-3 py-3 text-gray-600 whitespace-nowrap">
                  {row.mttr_hours ?? row.mttr ?? '—'}
                </td>
                <td className="px-3 py-3 text-gray-600 whitespace-nowrap">
                  {row.recommended_sla ?? '—'}
                </td>
                <td className="px-3 py-3 whitespace-nowrap">
                  {row.risk_level ? (
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${
                        row.risk_level === 'HIGH' || row.risk_level === 'CRITICAL'
                          ? 'bg-red-100 text-red-800 border-red-200'
                          : row.risk_level === 'MEDIUM'
                          ? 'bg-amber-100 text-amber-800 border-amber-200'
                          : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                      }`}
                    >
                      {row.risk_level}
                    </span>
                  ) : (
                    '—'
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─── Tab 4 – Tech Radar ───────────────────────────────────────────────────────

const FALLBACK_RADAR = {
  adopt: ['OpenAI GPT-4o', 'UiPath RPA', 'Zapier', 'Make (Integromat)', 'Python Pandas'],
  trial: ['Claude 3.5 Sonnet', 'LangChain', 'CrewAI', 'Vertex AI', 'Azure AI Studio'],
  assess: ['AutoGen', 'Semantic Kernel', 'Dify.ai', 'n8n', 'IBM watsonx'],
  hold: ['Legacy RPA (v1)', 'Rule-Based Chatbots', 'Proprietary ML Pipelines'],
};

const QUADRANT_CONFIG = [
  {
    key: 'adopt',
    label: 'Adopt Now',
    bg: 'bg-emerald-50 border-emerald-200',
    header: 'bg-emerald-600',
    badge: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    icon: ShieldCheck,
  },
  {
    key: 'trial',
    label: 'Trial',
    bg: 'bg-blue-50 border-blue-200',
    header: 'bg-blue-600',
    badge: 'bg-blue-100 text-blue-800 border-blue-200',
    icon: Radio,
  },
  {
    key: 'assess',
    label: 'Assess',
    bg: 'bg-amber-50 border-amber-200',
    header: 'bg-amber-500',
    badge: 'bg-amber-100 text-amber-800 border-amber-200',
    icon: Layers,
  },
  {
    key: 'hold',
    label: 'Hold',
    bg: 'bg-red-50 border-red-200',
    header: 'bg-red-500',
    badge: 'bg-red-100 text-red-800 border-red-200',
    icon: AlertTriangle,
  },
];

function groupByQuadrant(radarItems) {
  const groups = { adopt: [], trial: [], assess: [], hold: [] };
  if (!radarItems) return groups;
  radarItems.forEach((item) => {
    const q = (item.quadrant ?? '').toLowerCase().replace(/\s+/g, '_');
    if (q.includes('adopt')) groups.adopt.push(item.technology ?? item.name ?? item);
    else if (q.includes('trial')) groups.trial.push(item.technology ?? item.name ?? item);
    else if (q.includes('assess')) groups.assess.push(item.technology ?? item.name ?? item);
    else if (q.includes('hold')) groups.hold.push(item.technology ?? item.name ?? item);
  });
  return groups;
}

function TechRadarTab() {
  const { data: radarData, loading: radarLoading, error: radarError } = useApi(getTechRadar, []);
  const { data: adoptNow } = useApi(getTechAdoptNow, []);

  if (radarLoading) return <LoadingCards count={4} className="grid-cols-2" />;

  const grouped = radarData?.length
    ? groupByQuadrant(radarData)
    : FALLBACK_RADAR;

  // Merge adopt-now overrides
  if (adoptNow?.length) {
    adoptNow.forEach((t) => {
      const name = t.technology ?? t.name ?? t;
      if (!grouped.adopt.includes(name)) grouped.adopt.unshift(name);
    });
  }

  return (
    <div className="space-y-4">
      {radarError && (
        <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 rounded-lg px-4 py-2 text-sm text-amber-700">
          <AlertTriangle className="h-4 w-4 shrink-0" />
          Could not load live radar — showing curated fallback.
        </div>
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {QUADRANT_CONFIG.map(({ key, label, bg, header, badge, icon: Icon }) => {
          const items = grouped[key] ?? [];
          return (
            <Card key={key} className={`shadow-sm rounded-xl border ${bg}`}>
              <div className={`${header} rounded-t-xl px-4 py-3 flex items-center gap-2`}>
                <Icon className="h-4 w-4 text-white" />
                <span className="text-sm font-semibold text-white">{label}</span>
                <span className="ml-auto text-xs text-white/70">{items.length} technologies</span>
              </div>
              <CardContent className="p-4">
                {items.length === 0 ? (
                  <p className="text-xs text-gray-400">No technologies in this quadrant.</p>
                ) : (
                  <div className="flex flex-wrap gap-1.5">
                    {items.map((tech, j) => (
                      <span
                        key={j}
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${badge}`}
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

// ─── Page Root ────────────────────────────────────────────────────────────────

export default function VendorIntelligence() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Cpu className="h-6 w-6 text-violet-600" />
            Vendor Intelligence
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Compare AI tools, TCO, failure rates, and technology radar.
          </p>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="ai-tools">
          <TabsList className="bg-white border shadow-sm rounded-xl h-auto p-1 flex flex-wrap gap-1">
            <TabsTrigger value="ai-tools" className="rounded-lg text-sm">
              AI Tools
            </TabsTrigger>
            <TabsTrigger value="tco" className="rounded-lg text-sm">
              TCO Analysis
            </TabsTrigger>
            <TabsTrigger value="failure" className="rounded-lg text-sm">
              Failure Rates
            </TabsTrigger>
            <TabsTrigger value="radar" className="rounded-lg text-sm">
              Tech Radar
            </TabsTrigger>
          </TabsList>

          <TabsContent value="ai-tools" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Cpu className="h-5 w-5 text-violet-600" />
                  AI Tools Catalog
                </CardTitle>
              </CardHeader>
              <CardContent>
                <AIToolsTab />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="tco" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Layers className="h-5 w-5 text-violet-600" />
                  Total Cost of Ownership Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <TCOTab />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="failure" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-violet-600" />
                  Automation Failure Rate Intelligence
                </CardTitle>
              </CardHeader>
              <CardContent>
                <FailureRatesTab />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="radar" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Radar className="h-5 w-5 text-violet-600" />
                  Technology Radar
                </CardTitle>
                <p className="text-sm text-gray-500 mt-0.5">
                  Where each technology sits in the adoption lifecycle.
                </p>
              </CardHeader>
              <CardContent>
                <TechRadarTab />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
