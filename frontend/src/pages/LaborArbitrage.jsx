import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  TrendingUp, TrendingDown, AlertTriangle, Zap, Clock, Users, DollarSign, Star
} from 'lucide-react';
import { useApi } from '@/hooks/useApi';
import {
  getArbitrageAll,
  getArbitrageCritical,
  getAdoptionVelocity,
  getFirstMoverWindows,
} from '@/lib/api';
import { MetricCard } from '@/components/shared/MetricCard';
import { ScoreBar } from '@/components/shared/ScoreBadge';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';

// ─── Helpers ──────────────────────────────────────────────────────────────────

function urgencyClass(urgency) {
  const u = (urgency ?? '').toUpperCase();
  if (u === 'CRITICAL') return 'bg-red-100 text-red-800 border-red-200';
  if (u === 'HIGH') return 'bg-amber-100 text-amber-800 border-amber-200';
  if (u === 'MEDIUM') return 'bg-blue-100 text-blue-800 border-blue-200';
  return 'bg-emerald-100 text-emerald-800 border-emerald-200';
}

function windowUrgencyClass(months) {
  if (months < 3) return 'bg-red-100 text-red-800 border-red-200';
  if (months <= 6) return 'bg-amber-100 text-amber-800 border-amber-200';
  return 'bg-blue-100 text-blue-800 border-blue-200';
}

function formatCurrency(val) {
  if (val == null) return '—';
  const n = Number(val);
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(0)}k`;
  return `$${n.toFixed(0)}`;
}

const URGENCY_FILTERS = ['All', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];

// ─── KPI Row ──────────────────────────────────────────────────────────────────

function KPIRow({ arbitrageCritical, arbitrageAll, firstMoverWindows }) {
  const criticalCount = arbitrageCritical?.length ?? 0;

  const avgScore = useMemo(() => {
    if (!arbitrageAll?.length) return null;
    const total = arbitrageAll.reduce((sum, r) => sum + (r.arbitrage_score ?? r.score ?? 0), 0);
    return (total / arbitrageAll.length).toFixed(1);
  }, [arbitrageAll]);

  const closingSoon = useMemo(() => {
    if (!firstMoverWindows) return 0;
    return firstMoverWindows.filter((w) => (w.window_months ?? 99) < 6).length;
  }, [firstMoverWindows]);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <MetricCard
        title="Critical Opportunities"
        value={criticalCount}
        subtitle="Automate immediately"
        icon={AlertTriangle}
        color="red"
      />
      <MetricCard
        title="Avg Arbitrage Score"
        value={avgScore != null ? `${avgScore}/100` : '—'}
        subtitle="Across all tracked occupations"
        icon={TrendingUp}
        color="violet"
      />
      <MetricCard
        title="Windows Closing Soon"
        value={closingSoon}
        subtitle="First-mover windows under 6 months"
        icon={Clock}
        color="amber"
      />
    </div>
  );
}

// ─── Tab 1 – Automate Now ─────────────────────────────────────────────────────

function AutomateNowTab({ arbitrageAll, allLoading, allError, refetchAll }) {
  const [urgencyFilter, setUrgencyFilter] = useState('All');

  const filtered = useMemo(() => {
    if (!arbitrageAll) return [];
    const list = urgencyFilter === 'All'
      ? arbitrageAll
      : arbitrageAll.filter((r) => (r.urgency ?? '').toUpperCase() === urgencyFilter);
    return [...list].sort(
      (a, b) => (b.arbitrage_score ?? b.score ?? 0) - (a.arbitrage_score ?? a.score ?? 0)
    );
  }, [arbitrageAll, urgencyFilter]);

  if (allLoading) return <LoadingTable rows={8} cols={5} />;
  if (allError) return <ErrorState error={allError} onRetry={refetchAll} />;

  return (
    <div className="space-y-4">
      {/* Filter buttons */}
      <div className="flex flex-wrap gap-2">
        {URGENCY_FILTERS.map((f) => (
          <Button
            key={f}
            size="sm"
            variant={urgencyFilter === f ? 'default' : 'outline'}
            className={
              urgencyFilter === f
                ? 'bg-violet-600 hover:bg-violet-700 text-white h-8 text-xs'
                : 'h-8 text-xs text-gray-600 hover:text-violet-600 hover:border-violet-300'
            }
            onClick={() => setUrgencyFilter(f)}
          >
            {f}
          </Button>
        ))}
        <span className="text-xs text-gray-400 self-center ml-1">{filtered.length} occupations</span>
      </div>

      {!filtered.length ? (
        <p className="text-sm text-gray-400 py-8 text-center">No occupations match this filter.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-gray-50">
                {['Occupation', 'Arbitrage Score', 'Urgency', 'Wage Growth %', 'Labor Shortage'].map(
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
              {filtered.map((row, i) => {
                const score = row.arbitrage_score ?? row.score ?? 0;
                const urgency = row.urgency ?? '';
                const wageGrowth = row.wage_growth_pct ?? row.wage_growth ?? null;
                const shortage = row.labor_shortage ?? row.shortage ?? null;
                return (
                  <tr key={i} className="border-b hover:bg-gray-50 transition-colors">
                    <td className="px-3 py-3 font-medium text-gray-900 max-w-[200px] truncate">
                      {row.occupation ?? row.occupation_name ?? '—'}
                    </td>
                    <td className="px-3 py-3 min-w-[140px]">
                      <ScoreBar score={score} />
                    </td>
                    <td className="px-3 py-3 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${urgencyClass(
                          urgency
                        )}`}
                      >
                        {urgency || '—'}
                      </span>
                    </td>
                    <td className="px-3 py-3 whitespace-nowrap">
                      {wageGrowth != null ? (
                        <span className="flex items-center gap-1">
                          {wageGrowth > 0 ? (
                            <TrendingUp className="h-3.5 w-3.5 text-emerald-500" />
                          ) : (
                            <TrendingDown className="h-3.5 w-3.5 text-red-500" />
                          )}
                          <span
                            className={
                              wageGrowth > 0 ? 'text-emerald-700 font-medium' : 'text-red-700 font-medium'
                            }
                          >
                            {wageGrowth > 0 ? '+' : ''}
                            {wageGrowth}%
                          </span>
                        </span>
                      ) : (
                        <span className="text-gray-400">—</span>
                      )}
                    </td>
                    <td className="px-3 py-3 whitespace-nowrap">
                      {shortage != null ? (
                        <Badge variant="outline" className="text-xs font-normal">
                          {typeof shortage === 'boolean' ? (shortage ? 'Yes' : 'No') : shortage}
                        </Badge>
                      ) : (
                        <span className="text-gray-400">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ─── Tab 2 – Adoption Velocity ────────────────────────────────────────────────

const SIZE_ORDER = ['Startup', 'SMB', 'Mid-Market', 'Enterprise', 'Mega Corp'];

function AdoptionVelocityTab() {
  const { data, loading, error, refetch } = useApi(getAdoptionVelocity, []);

  if (loading) return <LoadingCards count={5} className="grid-cols-1 sm:grid-cols-2 lg:grid-cols-3" />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!data?.length) return (
    <p className="text-sm text-gray-400 py-8 text-center">No adoption velocity data available.</p>
  );

  const sorted = [...data].sort((a, b) => {
    const ai = SIZE_ORDER.indexOf(a.company_size ?? a.size ?? '');
    const bi = SIZE_ORDER.indexOf(b.company_size ?? b.size ?? '');
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-500">
        How fast different company sizes can pilot and scale AI automation.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {sorted.map((item, i) => {
          const size = item.company_size ?? item.size ?? `Tier ${i + 1}`;
          const pilotMonths = item.pilot_months ?? item.time_to_pilot ?? null;
          const scaleMonths = item.scale_months ?? item.time_to_scale ?? null;
          const successRate = item.success_rate ?? null;
          const typicalBudget = item.typical_budget ?? item.budget ?? null;
          const blockers = item.biggest_blockers ?? item.blockers ?? [];

          return (
            <Card key={i} className="bg-white shadow-sm rounded-xl border hover:shadow-md transition-shadow">
              <CardContent className="p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <p className="text-base font-bold text-gray-900">{size}</p>
                  <Users className="h-4 w-4 text-gray-300" />
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-violet-50 rounded-lg p-2.5 border border-violet-100 text-center">
                    <p className="text-violet-500 font-medium">Pilot → Scale</p>
                    <p className="text-violet-800 font-bold mt-0.5 text-sm">
                      {pilotMonths != null && scaleMonths != null
                        ? `${pilotMonths}–${scaleMonths}mo`
                        : pilotMonths != null
                        ? `${pilotMonths}mo`
                        : '—'}
                    </p>
                  </div>
                  <div className="bg-emerald-50 rounded-lg p-2.5 border border-emerald-100 text-center">
                    <p className="text-emerald-500 font-medium">Success Rate</p>
                    <p className="text-emerald-800 font-bold mt-0.5 text-sm">
                      {successRate != null
                        ? `${typeof successRate === 'number' && successRate <= 1
                            ? (successRate * 100).toFixed(0)
                            : successRate}%`
                        : '—'}
                    </p>
                  </div>
                </div>

                {typicalBudget != null && (
                  <div className="flex items-center gap-1.5 text-xs text-gray-600">
                    <DollarSign className="h-3.5 w-3.5 text-gray-400" />
                    <span>Typical Budget:</span>
                    <span className="font-semibold text-gray-900">
                      {typeof typicalBudget === 'string' ? typicalBudget : formatCurrency(typicalBudget)}
                    </span>
                  </div>
                )}

                {Array.isArray(blockers) && blockers.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1.5 font-medium">Biggest Blockers</p>
                    <div className="flex flex-wrap gap-1">
                      {blockers.map((b, j) => (
                        <span
                          key={j}
                          className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-700 border border-gray-200"
                        >
                          {b}
                        </span>
                      ))}
                    </div>
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

// ─── Tab 3 – First-Mover Windows ──────────────────────────────────────────────

function FirstMoverTab() {
  const navigate = useNavigate();
  const { data, loading, error, refetch } = useApi(getFirstMoverWindows, []);

  if (loading) return <LoadingCards count={6} className="grid-cols-1 sm:grid-cols-2 lg:grid-cols-3" />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!data?.length) return (
    <p className="text-sm text-gray-400 py-8 text-center">No first-mover window data available.</p>
  );

  const sorted = [...data].sort((a, b) => (a.window_months ?? 99) - (b.window_months ?? 99));

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-500">
        Act before these competitive windows close. First movers gain a significant ROI advantage.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {sorted.map((item, i) => {
          const windowMonths = item.window_months ?? null;
          const automationType = item.automation_type ?? item.type ?? item.name ?? '—';
          const advantage = item.competitive_advantage ?? item.advantage ?? null;
          const roiBonus = item.roi_bonus_pct ?? item.roi_bonus ?? null;

          return (
            <Card
              key={i}
              className={`shadow-sm rounded-xl border hover:shadow-md transition-shadow ${
                windowMonths != null && windowMonths < 3
                  ? 'border-red-200 bg-red-50/30'
                  : windowMonths != null && windowMonths <= 6
                  ? 'border-amber-200 bg-amber-50/20'
                  : 'bg-white'
              }`}
            >
              <CardContent className="p-5 space-y-3">
                {/* Header row */}
                <div className="flex items-start justify-between gap-2">
                  <p className="text-sm font-bold text-gray-900 leading-snug">{automationType}</p>
                  {windowMonths != null && (
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border shrink-0 ${windowUrgencyClass(
                        windowMonths
                      )}`}
                    >
                      {windowMonths < 3 ? (
                        <AlertTriangle className="h-3 w-3 mr-1" />
                      ) : (
                        <Clock className="h-3 w-3 mr-1" />
                      )}
                      {windowMonths}mo left
                    </span>
                  )}
                </div>

                {/* Competitive advantage */}
                {advantage && (
                  <p className="text-xs text-gray-600 leading-relaxed">{advantage}</p>
                )}

                {/* ROI bonus */}
                {roiBonus != null && (
                  <div className="flex items-center gap-1.5 bg-emerald-50 rounded-lg px-3 py-2 border border-emerald-100">
                    <Star className="h-3.5 w-3.5 text-emerald-600" />
                    <span className="text-xs text-emerald-700 font-medium">
                      First-mover ROI bonus:{' '}
                      <span className="font-bold">
                        +{typeof roiBonus === 'number' && roiBonus <= 1
                          ? (roiBonus * 100).toFixed(0)
                          : roiBonus}%
                      </span>
                    </span>
                  </div>
                )}

                {/* CTA */}
                <Button
                  size="sm"
                  className="w-full bg-violet-600 hover:bg-violet-700 text-white text-xs h-8 mt-1"
                  onClick={() => navigate('/build/wizard')}
                >
                  <Zap className="h-3.5 w-3.5 mr-1.5" />
                  Start Building →
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

// ─── Page Root ────────────────────────────────────────────────────────────────

export default function LaborArbitrage() {
  const {
    data: arbitrageAll,
    loading: allLoading,
    error: allError,
    refetch: refetchAll,
  } = useApi(getArbitrageAll, []);

  const { data: arbitrageCritical } = useApi(getArbitrageCritical, []);
  const { data: firstMoverWindows } = useApi(getFirstMoverWindows, []);

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-violet-600" />
            Labor Arbitrage Intelligence
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Identify automation opportunities before the window closes.
          </p>
        </div>

        {/* KPI Row */}
        <KPIRow
          arbitrageCritical={arbitrageCritical}
          arbitrageAll={arbitrageAll}
          firstMoverWindows={firstMoverWindows}
        />

        {/* Tabs */}
        <Tabs defaultValue="automate-now">
          <TabsList className="bg-white border shadow-sm rounded-xl h-auto p-1 flex flex-wrap gap-1">
            <TabsTrigger value="automate-now" className="rounded-lg text-sm">
              Automate Now
            </TabsTrigger>
            <TabsTrigger value="velocity" className="rounded-lg text-sm">
              Adoption Velocity
            </TabsTrigger>
            <TabsTrigger value="windows" className="rounded-lg text-sm">
              First-Mover Windows
            </TabsTrigger>
          </TabsList>

          <TabsContent value="automate-now" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Zap className="h-5 w-5 text-violet-600" />
                  Automate Now
                </CardTitle>
                <p className="text-sm text-gray-500 mt-0.5">
                  Occupations ranked by arbitrage score. Act on CRITICAL items immediately.
                </p>
              </CardHeader>
              <CardContent>
                <AutomateNowTab
                  arbitrageAll={arbitrageAll}
                  allLoading={allLoading}
                  allError={allError}
                  refetchAll={refetchAll}
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="velocity" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Users className="h-5 w-5 text-violet-600" />
                  Adoption Velocity
                </CardTitle>
                <p className="text-sm text-gray-500 mt-0.5">
                  How fast different companies can scale AI automation.
                </p>
              </CardHeader>
              <CardContent>
                <AdoptionVelocityTab />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="windows" className="mt-6">
            <Card className="bg-white shadow-sm rounded-xl border">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5 text-violet-600" />
                  Act Before These Windows Close
                </CardTitle>
                <p className="text-sm text-gray-500 mt-0.5">
                  First-mover advantages are time-limited. Sorted by urgency.
                </p>
              </CardHeader>
              <CardContent>
                <FirstMoverTab />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
