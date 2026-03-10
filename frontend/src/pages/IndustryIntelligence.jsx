import { useMemo } from 'react';
import { Factory, TrendingUp, TrendingDown, Award, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';
import { MetricCard } from '@/components/shared/MetricCard';
import { useApi } from '@/hooks/useApi';
import {
  getAllIndustries,
  getIndustryRankings,
  getDisruptionForecast,
  getMostDisrupted,
  getSafestIndustries,
  getAutomationLeaders,
} from '@/lib/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

function maturityColor(score) {
  if (score > 70) return '#10b981'; // emerald
  if (score >= 50) return '#3b82f6'; // blue
  return '#f59e0b'; // amber
}

function maturityLabel(score) {
  if (score > 70) return 'Leading';
  if (score >= 50) return 'Advancing';
  return 'Early Stage';
}

function maturityBadgeClass(score) {
  if (score > 70) return 'bg-emerald-100 text-emerald-800 border-emerald-200';
  if (score >= 50) return 'bg-blue-100 text-blue-800 border-blue-200';
  return 'bg-amber-100 text-amber-800 border-amber-200';
}

function getScore(industry) {
  return (
    industry.maturity_score ??
    industry.automation_maturity_score ??
    industry.score ??
    industry.automation_score ??
    0
  );
}

function getName(industry) {
  return industry.industry_name ?? industry.industry ?? industry.name ?? '—';
}

// Custom bar label for chart
function CustomBarLabel({ x, y, width, value }) {
  return (
    <text
      x={x + width + 4}
      y={y + 12}
      fill="#6b7280"
      fontSize={10}
      textAnchor="start"
    >
      {value}
    </text>
  );
}

// ── Top Chart: Horizontal BarChart ─────────────────────────────────────────

function MaturityChart({ industries, loading, error }) {
  const chartData = useMemo(() => {
    if (!industries?.length) return [];
    return [...industries]
      .sort((a, b) => getScore(b) - getScore(a))
      .slice(0, 20)
      .map((ind) => ({
        name: getName(ind),
        score: Math.round(getScore(ind)),
        fill: maturityColor(getScore(ind)),
      }));
  }, [industries]);

  if (loading)
    return (
      <Card className="border shadow-sm rounded-xl bg-white">
        <CardContent className="p-6">
          <div className="h-[300px] flex items-center justify-center text-muted-foreground text-sm">
            Loading chart...
          </div>
        </CardContent>
      </Card>
    );

  if (error || !chartData.length) return null;

  return (
    <Card className="border shadow-sm rounded-xl bg-white">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold">Industry Automation Maturity Rankings</CardTitle>
        <p className="text-xs text-muted-foreground">Score 0–100 · Emerald = Leading (&gt;70) · Blue = Advancing (50–70) · Amber = Early Stage (&lt;50)</p>
      </CardHeader>
      <CardContent className="pr-8">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 4, right: 48, left: 4, bottom: 4 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0f0f0" />
            <XAxis
              type="number"
              domain={[0, 100]}
              tick={{ fontSize: 10 }}
              tickLine={false}
            />
            <YAxis
              type="category"
              dataKey="name"
              width={140}
              tick={{ fontSize: 10 }}
              tickLine={false}
            />
            <Tooltip
              formatter={(value) => [value, 'Maturity Score']}
              contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 12 }}
            />
            <Bar dataKey="score" radius={[0, 4, 4, 0]} label={<CustomBarLabel />}>
              {chartData.map((entry, idx) => (
                <Cell key={idx} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

// ── Tab 1: Maturity Rankings ───────────────────────────────────────────────

function MaturityRankingsTab({ industries, rankings, loading, error, refetch }) {
  const sorted = useMemo(() => {
    const source = rankings?.length ? rankings : industries ?? [];
    return [...source].sort((a, b) => getScore(b) - getScore(a));
  }, [industries, rankings]);

  if (loading) return <LoadingTable rows={10} cols={4} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!sorted.length)
    return <p className="text-sm text-muted-foreground py-8 text-center">No industry data available.</p>;

  return (
    <div className="rounded-xl border bg-white overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-gray-50 text-xs text-muted-foreground uppercase tracking-wide">
              <th className="text-center px-4 py-3 font-medium w-12">Rank</th>
              <th className="text-left px-4 py-3 font-medium">Industry</th>
              <th className="text-left px-4 py-3 font-medium min-w-[160px]">Maturity Score</th>
              <th className="text-left px-4 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((ind, idx) => {
              const score = Math.round(getScore(ind));
              return (
                <tr key={ind.id ?? idx} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 text-center">
                    <span className="text-sm font-bold text-muted-foreground">#{idx + 1}</span>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-foreground">{getName(ind)}</p>
                    {ind.key_leader && (
                      <p className="text-xs text-muted-foreground mt-0.5">Leader: {ind.key_leader}</p>
                    )}
                  </td>
                  <td className="px-4 py-3 min-w-[160px]">
                    <div className="flex items-center gap-2">
                      <Progress value={score} className="h-2 flex-1" />
                      <span className="text-xs font-semibold tabular-nums w-6">{score}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${maturityBadgeClass(score)}`}>
                      {maturityLabel(score)}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── Tab 2: Disruption Forecast ─────────────────────────────────────────────

function DisruptionForecastTab({ forecast, mostDisrupted, safest, loading, error, refetch }) {
  const allItems = useMemo(() => {
    const source = forecast?.length ? forecast : [];
    return [...source].sort((a, b) => {
      const ja = a.job_change_pct ?? a.disruption_score ?? 0;
      const jb = b.job_change_pct ?? b.disruption_score ?? 0;
      return ja - jb; // most negative (disrupted) first
    });
  }, [forecast]);

  const top3Disrupted = useMemo(() => {
    if (mostDisrupted?.length) return mostDisrupted.slice(0, 3);
    return allItems.slice(0, 3);
  }, [mostDisrupted, allItems]);

  const top3Safest = useMemo(() => {
    if (safest?.length) return safest.slice(0, 3);
    return [...allItems].reverse().slice(0, 3);
  }, [safest, allItems]);

  const midItems = useMemo(() => {
    if (!allItems.length) return [];
    const disruptedNames = new Set(top3Disrupted.map(getName));
    const safestNames = new Set(top3Safest.map(getName));
    return allItems.filter((i) => !disruptedNames.has(getName(i)) && !safestNames.has(getName(i)));
  }, [allItems, top3Disrupted, top3Safest]);

  if (loading) return <LoadingCards count={6} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  function DisruptionCard({ industry, highlight }) {
    const name = getName(industry);
    const pct = industry.job_change_pct ?? industry.disruption_score ?? industry.change_pct;
    const isNeg = pct != null && pct < 0;
    const isPos = pct != null && pct > 0;
    return (
      <Card className={`border shadow-sm rounded-xl bg-white ${highlight === 'danger' ? 'border-red-200 bg-red-50' : highlight === 'safe' ? 'border-emerald-200 bg-emerald-50' : ''}`}>
        <CardContent className="p-4">
          <p className="font-semibold text-sm text-foreground">{name}</p>
          {pct != null && (
            <p className={`text-xl font-bold mt-1 ${isNeg ? 'text-red-600' : isPos ? 'text-emerald-600' : 'text-gray-600'}`}>
              {pct > 0 ? '+' : ''}{typeof pct === 'number' ? pct.toFixed(1) : pct}%
            </p>
          )}
          <p className="text-xs text-muted-foreground mt-1">
            {isNeg ? 'Job displacement forecast' : isPos ? 'Job growth forecast' : 'Forecast change'}
          </p>
          {industry.timeline_years && (
            <p className="text-xs text-muted-foreground">{industry.timeline_years}-year horizon</p>
          )}
        </CardContent>
      </Card>
    );
  }

  const hasData = top3Disrupted.length > 0 || top3Safest.length > 0 || midItems.length > 0;

  if (!hasData)
    return <p className="text-sm text-muted-foreground py-8 text-center">No disruption forecast data available.</p>;

  return (
    <div className="space-y-6">
      {/* Most disrupted */}
      {top3Disrupted.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3">
            <TrendingDown className="h-4 w-4 text-red-500" />
            <h3 className="text-sm font-semibold text-red-700 uppercase tracking-wide">Most Disrupted</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {top3Disrupted.map((ind, idx) => (
              <DisruptionCard key={ind.id ?? idx} industry={ind} highlight="danger" />
            ))}
          </div>
        </div>
      )}

      {/* Middle industries */}
      {midItems.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">All Industries</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {midItems.map((ind, idx) => (
              <DisruptionCard key={ind.id ?? idx} industry={ind} />
            ))}
          </div>
        </div>
      )}

      {/* Safest industries */}
      {top3Safest.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="h-4 w-4 text-emerald-500" />
            <h3 className="text-sm font-semibold text-emerald-700 uppercase tracking-wide">Safest Industries</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {top3Safest.map((ind, idx) => (
              <DisruptionCard key={ind.id ?? idx} industry={ind} highlight="safe" />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Tab 3: Competitive Leaders ─────────────────────────────────────────────

function CompetitiveLeadersTab({ leaders, industries, loading, error, refetch }) {
  const hasLeaders = leaders?.length > 0;

  // Calculate average adoption for gap display
  const avgAdoption = useMemo(() => {
    if (!leaders?.length) return null;
    const vals = leaders
      .map((l) => l.adoption_pct ?? l.adoption_percentage ?? l.adoption_level ?? null)
      .filter((v) => v != null && typeof v === 'number');
    if (!vals.length) return null;
    return vals.reduce((a, b) => a + b, 0) / vals.length;
  }, [leaders]);

  if (loading) return <LoadingCards count={8} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  if (!hasLeaders) {
    // Fallback: show early adopters vs laggards from industries
    const sorted = industries?.length
      ? [...industries].sort((a, b) => getScore(b) - getScore(a))
      : [];
    const earlyAdopters = sorted.slice(0, 5);
    const laggards = sorted.slice(-5).reverse();

    if (!sorted.length)
      return <p className="text-sm text-muted-foreground py-8 text-center">No leader data available.</p>;

    return (
      <div className="space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Award className="h-4 w-4 text-violet-600" />
            <h3 className="text-sm font-semibold text-violet-700 uppercase tracking-wide">Early Adopters</h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {earlyAdopters.map((ind, idx) => {
              const score = Math.round(getScore(ind));
              return (
                <Card key={ind.id ?? idx} className="border border-violet-200 shadow-sm rounded-xl bg-white">
                  <CardContent className="p-4">
                    <p className="font-semibold text-sm text-foreground">{getName(ind)}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Progress value={score} className="h-2 flex-1" />
                      <span className={`text-sm font-bold ${score > 70 ? 'text-emerald-600' : 'text-blue-600'}`}>{score}</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">{maturityLabel(score)}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-3">
            <TrendingDown className="h-4 w-4 text-amber-500" />
            <h3 className="text-sm font-semibold text-amber-700 uppercase tracking-wide">Laggards</h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {laggards.map((ind, idx) => {
              const score = Math.round(getScore(ind));
              return (
                <Card key={ind.id ?? idx} className="border border-amber-200 shadow-sm rounded-xl bg-white">
                  <CardContent className="p-4">
                    <p className="font-semibold text-sm text-foreground">{getName(ind)}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Progress value={score} className="h-2 flex-1" />
                      <span className="text-sm font-bold text-amber-600">{score}</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">{maturityLabel(score)}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {avgAdoption != null && (
        <Card className="border shadow-sm rounded-xl bg-violet-50 border-violet-200">
          <CardContent className="p-4 flex items-center gap-4">
            <Users className="h-6 w-6 text-violet-600 shrink-0" />
            <div>
              <p className="text-sm font-semibold text-violet-800">Average Industry Adoption</p>
              <p className="text-2xl font-bold text-violet-700">{avgAdoption.toFixed(1)}%</p>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {leaders.map((leader, idx) => {
          const adoption = leader.adoption_pct ?? leader.adoption_percentage ?? leader.adoption_level;
          const adoptionNum = typeof adoption === 'number' ? adoption : parseFloat(adoption);
          const vsAvg = avgAdoption != null && !isNaN(adoptionNum) ? adoptionNum - avgAdoption : null;
          return (
            <Card key={leader.id ?? idx} className="border shadow-sm rounded-xl bg-white hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-start justify-between gap-2 mb-2">
                  <p className="font-semibold text-sm text-foreground flex-1">
                    {leader.industry ?? leader.sector ?? leader.industry_name ?? '—'}
                  </p>
                  {leader.rank != null && (
                    <span className="text-xs font-bold text-violet-600 shrink-0">#{leader.rank}</span>
                  )}
                </div>

                {(leader.leader_company ?? leader.company ?? leader.top_company) && (
                  <div className="flex items-center gap-1.5 mb-2">
                    <Award className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                    <p className="text-xs font-medium text-foreground">
                      {leader.leader_company ?? leader.company ?? leader.top_company}
                    </p>
                  </div>
                )}

                {!isNaN(adoptionNum) && (
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-muted-foreground">Adoption Level</span>
                      <span className="text-xs font-bold">{adoptionNum.toFixed(0)}%</span>
                    </div>
                    <Progress value={adoptionNum} className="h-1.5" />
                  </div>
                )}

                {vsAvg != null && (
                  <p className={`text-xs mt-2 font-medium ${vsAvg >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                    {vsAvg >= 0 ? '+' : ''}{vsAvg.toFixed(1)}% vs average
                  </p>
                )}

                {leader.competitive_advantage && (
                  <p className="text-xs text-muted-foreground mt-2 leading-relaxed line-clamp-2">
                    {leader.competitive_advantage}
                  </p>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

// ── Main Component ─────────────────────────────────────────────────────────

export default function IndustryIntelligence() {
  const { data: industries, loading: indLoading, error: indError, refetch: indRefetch } = useApi(getAllIndustries, [], []);
  const { data: rankings, loading: rkLoading, error: rkError, refetch: rkRefetch } = useApi(getIndustryRankings, [], []);
  const { data: forecast, loading: fcLoading, error: fcError, refetch: fcRefetch } = useApi(getDisruptionForecast, [], []);
  const { data: mostDisrupted, loading: mdLoading } = useApi(getMostDisrupted, [10], []);
  const { data: safest, loading: sfLoading } = useApi(getSafestIndustries, [5], []);
  const { data: leaders, loading: ldLoading, error: ldError, refetch: ldRefetch } = useApi(getAutomationLeaders, [], []);

  const allIndustries = useMemo(() => {
    const src = industries ?? rankings ?? [];
    return Array.isArray(src) ? src : [];
  }, [industries, rankings]);

  const avgMaturity = useMemo(() => {
    if (!allIndustries.length) return null;
    const scores = allIndustries.map(getScore).filter((s) => s > 0);
    if (!scores.length) return null;
    return (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
  }, [allIndustries]);

  const leadingCount = useMemo(
    () => allIndustries.filter((i) => getScore(i) > 70).length,
    [allIndustries]
  );

  return (
    <div className="bg-gray-50 min-h-screen p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Industry Intelligence</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Automation maturity rankings, disruption forecasts, and competitive leader analysis
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Industries Tracked"
          value={indLoading ? '—' : String(allIndustries.length || 20)}
          subtitle="Across all sectors"
          icon={Factory}
          color="violet"
        />
        <MetricCard
          title="Avg Maturity Score"
          value={indLoading ? '—' : avgMaturity ? `${avgMaturity}/100` : '—'}
          subtitle="Industry-wide average"
          icon={TrendingUp}
          color="blue"
        />
        <MetricCard
          title="Leading Industries"
          value={indLoading ? '—' : String(leadingCount)}
          subtitle="Maturity score > 70"
          icon={Award}
          color="emerald"
        />
      </div>

      {/* Top chart */}
      <MaturityChart
        industries={allIndustries}
        loading={indLoading && rkLoading}
        error={indError && rkError}
      />

      {/* Tabs */}
      <Tabs defaultValue="rankings" className="space-y-4">
        <TabsList className="bg-white border rounded-lg p-1">
          <TabsTrigger value="rankings" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            Maturity Rankings
          </TabsTrigger>
          <TabsTrigger value="disruption" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            Disruption Forecast
          </TabsTrigger>
          <TabsTrigger value="leaders" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            Competitive Leaders
          </TabsTrigger>
        </TabsList>

        <TabsContent value="rankings">
          <MaturityRankingsTab
            industries={allIndustries}
            rankings={rankings}
            loading={indLoading || rkLoading}
            error={indError ?? rkError}
            refetch={() => { indRefetch(); rkRefetch(); }}
          />
        </TabsContent>

        <TabsContent value="disruption">
          <DisruptionForecastTab
            forecast={forecast}
            mostDisrupted={mostDisrupted}
            safest={safest}
            loading={fcLoading || mdLoading || sfLoading}
            error={fcError}
            refetch={fcRefetch}
          />
        </TabsContent>

        <TabsContent value="leaders">
          <CompetitiveLeadersTab
            leaders={leaders}
            industries={allIndustries}
            loading={ldLoading || indLoading}
            error={ldError}
            refetch={() => { ldRefetch(); indRefetch(); }}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
