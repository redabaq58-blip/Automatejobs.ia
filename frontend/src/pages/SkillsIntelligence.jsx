import { useState, useMemo } from 'react';
import { Brain, Users, TrendingDown, ArrowRight, Award, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { MetricCard } from '@/components/shared/MetricCard';
import { ThreatBadge } from '@/components/shared/ComplianceBadge';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';
import { useApi } from '@/hooks/useApi';
import {
  getSkillsAll,
  getWorkforceImpact,
  getReskillingAll,
  getReskillingHighestROI,
} from '@/lib/api';
import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

// ── Helpers ─────────────────────────────────────────────────────────────────

const THREAT_ORDER = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };

const THREAT_COLORS = {
  CRITICAL: '#ef4444',
  HIGH: '#f59e0b',
  MEDIUM: '#3b82f6',
  LOW: '#10b981',
};

function formatJobCount(n) {
  if (!n && n !== 0) return '—';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

function formatCurrency(n) {
  if (!n && n !== 0) return '—';
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function formatMarketValue(n) {
  if (!n && n !== 0) return '—';
  if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(0)}B`;
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function getROILabel(roi) {
  const num = typeof roi === 'string' ? parseFloat(roi) : roi;
  if (!num && num !== 0) return null;
  if (num > 200) return { label: `${num.toFixed(0)}%`, class: 'bg-emerald-100 text-emerald-800 border-emerald-200' };
  if (num >= 100) return { label: `${num.toFixed(0)}%`, class: 'bg-blue-100 text-blue-800 border-blue-200' };
  return { label: `${num.toFixed(0)}%`, class: 'bg-amber-100 text-amber-800 border-amber-200' };
}

// Progress bar width for skill half-life: ((half_life_years / 10) * 100) capped at 100
function halfLifeProgress(years) {
  if (!years && years !== 0) return 50;
  return Math.min(100, Math.max(0, (years / 10) * 100));
}

// ── Tab 1: Skills Decay ──────────────────────────────────────────────────────

function SkillsDecayTab({ skills, loading, error, refetch }) {
  const [filter, setFilter] = useState('ALL');

  const sorted = useMemo(() => {
    if (!skills) return [];
    return [...skills]
      .filter((s) => filter === 'ALL' || (s.automation_threat_level ?? s.threat_level) === filter)
      .sort((a, b) => {
        const la = a.automation_threat_level ?? a.threat_level;
        const lb = b.automation_threat_level ?? b.threat_level;
        const td = (THREAT_ORDER[la] ?? 9) - (THREAT_ORDER[lb] ?? 9);
        if (td !== 0) return td;
        return (b.jobs_at_risk_usa ?? 0) - (a.jobs_at_risk_usa ?? 0);
      });
  }, [skills, filter]);

  const counts = useMemo(() => {
    if (!skills) return {};
    return skills.reduce((acc, s) => {
      const level = s.automation_threat_level ?? s.threat_level ?? 'UNKNOWN';
      acc[level] = (acc[level] ?? 0) + 1;
      return acc;
    }, {});
  }, [skills]);

  if (loading) return <LoadingTable rows={8} cols={5} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!skills?.length)
    return (
      <p className="text-sm text-muted-foreground py-8 text-center">
        No skills data available.
      </p>
    );

  return (
    <div className="space-y-4">
      {/* Filter row */}
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-muted-foreground">Filter by threat level:</span>
        <Select value={filter} onValueChange={setFilter}>
          <SelectTrigger className="w-44 bg-white">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Levels ({skills.length})</SelectItem>
            {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
              <SelectItem key={lvl} value={lvl}>
                {lvl} ({counts[lvl] ?? 0})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <span className="text-xs text-muted-foreground ml-auto">
          Showing {sorted.length} skill{sorted.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Table */}
      <div className="rounded-xl border bg-white overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-gray-50 text-xs text-muted-foreground uppercase tracking-wide">
                <th className="text-left px-4 py-3 font-medium">Skill Name</th>
                <th className="text-left px-4 py-3 font-medium">Threat</th>
                <th className="text-right px-4 py-3 font-medium">Half-Life (yrs)</th>
                <th className="text-right px-4 py-3 font-medium">Jobs at Risk</th>
                <th className="text-right px-4 py-3 font-medium">5-yr Wage Impact</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((skill, idx) => {
                const level = skill.automation_threat_level ?? skill.threat_level;
                const progress = halfLifeProgress(skill.half_life_years);
                const wageImpact = skill.wage_impact_5yr_percent ?? skill.wage_impact_5yr;
                return (
                  <tr
                    key={skill.id ?? skill.skill_name ?? idx}
                    className="border-b last:border-0 hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-4 py-3 max-w-xs">
                      <p className="font-medium text-foreground truncate">{skill.skill_name ?? '—'}</p>
                      <div className="mt-1.5 flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-1.5 max-w-[140px]">
                          <div
                            className="h-1.5 rounded-full bg-amber-400 transition-all"
                            style={{ width: `${progress}%` }}
                          />
                        </div>
                        <span className="text-xs text-muted-foreground tabular-nums">
                          {progress.toFixed(0)}% remaining value
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <ThreatBadge level={level} />
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums">
                      {skill.half_life_years != null ? skill.half_life_years : '—'}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums font-medium">
                      {formatJobCount(skill.jobs_at_risk_usa)}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums">
                      {wageImpact != null
                        ? (
                          <span className={wageImpact < 0 ? 'text-red-600 font-medium' : 'text-emerald-600 font-medium'}>
                            {wageImpact > 0 ? '+' : ''}{wageImpact}%
                          </span>
                        )
                        : '—'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ── Tab 2: Reskilling Pathways ───────────────────────────────────────────────

function ReskillingTab({ pathways, topROI, loading, error, refetch }) {
  const sorted = useMemo(() => {
    if (!pathways) return [];
    return [...pathways].sort((a, b) => {
      const ra = typeof a.roi_score === 'string' ? parseFloat(a.roi_score) : (a.roi_score ?? 0);
      const rb = typeof b.roi_score === 'string' ? parseFloat(b.roi_score) : (b.roi_score ?? 0);
      return rb - ra;
    });
  }, [pathways]);

  const top3 = useMemo(() => {
    const source = topROI?.length ? topROI : sorted;
    return source.slice(0, 3);
  }, [topROI, sorted]);

  if (loading) return <LoadingTable rows={8} cols={5} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  return (
    <div className="space-y-6">
      {/* Top 3 Best ROI cards */}
      {top3.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-3">
            Highest ROI Transitions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {top3.map((p, idx) => {
              const roi = typeof p.roi_score === 'string' ? parseFloat(p.roi_score) : (p.roi_score ?? 0);
              const roiBadge = getROILabel(roi);
              const fromRole = p.from_role ?? p.current_role ?? '—';
              const toRole = p.to_role ?? p.target_role ?? '—';
              const durationMonths = p.duration_months ?? p.training_duration_months;
              const salaryIncrease = p.salary_increase_percent ?? p.salary_increase_pct;
              const cost = p.training_cost_usd;
              return (
                <Card key={p.id ?? idx} className="border shadow-sm rounded-xl bg-white hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-1.5 mb-3">
                      <Award className="h-4 w-4 text-emerald-600" />
                      <span className="text-xs font-semibold text-emerald-700">#{idx + 1} Best ROI</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-sm font-medium flex-wrap mb-3">
                      <span className="text-foreground">{fromRole}</span>
                      <ArrowRight className="h-3.5 w-3.5 text-emerald-600 shrink-0" />
                      <span className="text-emerald-700">{toRole}</span>
                    </div>
                    <div className="flex items-center gap-2 mb-2">
                      {roiBadge && (
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${roiBadge.class}`}>
                          {roiBadge.label} ROI
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-muted-foreground space-y-0.5">
                      {cost != null && <p>Cost: <span className="font-medium text-foreground">{formatCurrency(cost)}</span></p>}
                      {durationMonths != null && <p>Duration: <span className="font-medium text-foreground">{durationMonths} months</span></p>}
                      {salaryIncrease != null && <p>Salary increase: <span className="font-medium text-emerald-600">+{salaryIncrease}%</span></p>}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* Full pathways table */}
      {sorted.length > 0 ? (
        <div className="rounded-xl border bg-white overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-gray-50 text-xs text-muted-foreground uppercase tracking-wide">
                  <th className="text-left px-4 py-3 font-medium">From Role → To Role</th>
                  <th className="text-right px-4 py-3 font-medium">Cost</th>
                  <th className="text-right px-4 py-3 font-medium">Duration</th>
                  <th className="text-right px-4 py-3 font-medium">Salary ↑</th>
                  <th className="text-right px-4 py-3 font-medium">ROI Score</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map((p, idx) => {
                  const roi = typeof p.roi_score === 'string' ? parseFloat(p.roi_score) : (p.roi_score ?? null);
                  const roiBadge = getROILabel(roi);
                  const fromRole = p.from_role ?? p.current_role ?? '—';
                  const toRole = p.to_role ?? p.target_role ?? '—';
                  const durationMonths = p.duration_months ?? p.training_duration_months;
                  const salaryIncrease = p.salary_increase_percent ?? p.salary_increase_pct;
                  return (
                    <tr
                      key={p.id ?? idx}
                      className="border-b last:border-0 hover:bg-gray-50 transition-colors"
                    >
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="text-muted-foreground">{fromRole}</span>
                          <ArrowRight className="h-3.5 w-3.5 text-emerald-600 shrink-0" />
                          <span className="font-medium text-foreground">{toRole}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums">
                        {p.training_cost_usd != null ? formatCurrency(p.training_cost_usd) : '—'}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums">
                        {durationMonths != null ? `${durationMonths} mo` : '—'}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums">
                        {salaryIncrease != null ? (
                          <span className="text-emerald-600 font-medium">+{salaryIncrease}%</span>
                        ) : '—'}
                      </td>
                      <td className="px-4 py-3 text-right">
                        {roiBadge ? (
                          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${roiBadge.class}`}>
                            {roiBadge.label}
                          </span>
                        ) : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <p className="text-sm text-muted-foreground py-8 text-center">
          No reskilling pathway data available.
        </p>
      )}
    </div>
  );
}

// ── Tab 3: Workforce Impact ──────────────────────────────────────────────────

function WorkforceImpactTab({ skills, workforceImpact, loading, error, refetch }) {
  const chartData = useMemo(() => {
    if (!skills?.length) return [];
    const agg = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
    skills.forEach((s) => {
      const level = s.automation_threat_level ?? s.threat_level;
      if (agg[level] !== undefined) {
        agg[level] += s.jobs_at_risk_usa ?? 0;
      }
    });
    return [
      { name: 'CRITICAL', jobs: agg.CRITICAL, fill: '#ef4444' },
      { name: 'HIGH', jobs: agg.HIGH, fill: '#f59e0b' },
      { name: 'MEDIUM', jobs: agg.MEDIUM, fill: '#3b82f6' },
      { name: 'LOW', jobs: agg.LOW, fill: '#10b981' },
    ];
  }, [skills]);

  if (loading) return <LoadingCards count={3} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  const totalJobs = workforceImpact?.total_jobs_at_risk_usa ?? workforceImpact?.total_jobs_at_risk;
  const reskillingMarket = workforceImpact?.reskilling_market_value_usd;
  const skillsAnalyzed = workforceImpact?.skills_analyzed;

  return (
    <div className="space-y-6">
      {/* Summary stats from getWorkforceImpact */}
      {workforceImpact && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="border shadow-sm rounded-xl bg-gradient-to-br from-red-50 to-white">
            <CardContent className="p-5">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                Total Jobs at Risk (USA)
              </p>
              <p className="text-3xl font-bold text-red-600">
                {totalJobs ? formatJobCount(totalJobs) : '8.1M+'}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Automation-driven displacement
              </p>
            </CardContent>
          </Card>
          <Card className="border shadow-sm rounded-xl bg-gradient-to-br from-emerald-50 to-white">
            <CardContent className="p-5">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                Reskilling Market Value
              </p>
              <p className="text-3xl font-bold text-emerald-600">
                {reskillingMarket ? formatMarketValue(reskillingMarket) : '$94B'}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Global reskilling opportunity
              </p>
            </CardContent>
          </Card>
          <Card className="border shadow-sm rounded-xl bg-gradient-to-br from-violet-50 to-white">
            <CardContent className="p-5">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                Skills Analyzed
              </p>
              <p className="text-3xl font-bold text-violet-600">
                {skillsAnalyzed ?? skills?.length ?? '—'}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Across all threat levels
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Bar chart — jobs at risk by threat level */}
      <Card className="border shadow-sm rounded-xl bg-white">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">Jobs at Risk by Threat Level</CardTitle>
          <p className="text-xs text-muted-foreground">
            Aggregated across all skills in each automation threat category
          </p>
        </CardHeader>
        <CardContent>
          {chartData.some((d) => d.jobs > 0) ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData} margin={{ top: 8, right: 16, left: 8, bottom: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 12, fill: '#6b7280' }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tickFormatter={(v) => formatJobCount(v)}
                  tick={{ fontSize: 11, fill: '#6b7280' }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  formatter={(value) => [formatJobCount(value), 'Jobs at Risk']}
                  contentStyle={{
                    borderRadius: 8,
                    border: '1px solid #e5e7eb',
                    fontSize: 12,
                    boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                  }}
                  cursor={{ fill: 'rgba(0,0,0,0.04)' }}
                />
                <Bar dataKey="jobs" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, idx) => (
                    <Cell key={idx} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-muted-foreground text-center py-8">
              Chart data unavailable — skills data may still be loading.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Threat level legend */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { level: 'CRITICAL', color: 'bg-red-500', label: 'Critically threatened' },
          { level: 'HIGH', color: 'bg-amber-500', label: 'High displacement risk' },
          { level: 'MEDIUM', color: 'bg-blue-500', label: 'Moderate risk' },
          { level: 'LOW', color: 'bg-emerald-500', label: 'Lower risk' },
        ].map(({ level, color, label }) => {
          const count = skills?.filter((s) => (s.automation_threat_level ?? s.threat_level) === level).length ?? 0;
          return (
            <div key={level} className="flex items-start gap-2.5 p-3 rounded-lg border bg-white">
              <div className={`h-3 w-3 rounded-full ${color} shrink-0 mt-0.5`} />
              <div>
                <p className="text-xs font-semibold text-foreground">{level}</p>
                <p className="text-xs text-muted-foreground">{label}</p>
                <p className="text-sm font-bold text-foreground mt-0.5">{count} skills</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Main Component ───────────────────────────────────────────────────────────

export default function SkillsIntelligence() {
  const {
    data: skills,
    loading: skillsLoading,
    error: skillsError,
    refetch: skillsRefetch,
  } = useApi(getSkillsAll, [], []);

  const {
    data: workforceImpact,
    loading: wfLoading,
    error: wfError,
    refetch: wfRefetch,
  } = useApi(getWorkforceImpact, [], []);

  const {
    data: pathways,
    loading: pathwaysLoading,
    error: pathwaysError,
    refetch: pathwaysRefetch,
  } = useApi(getReskillingAll, [], []);

  const {
    data: topROI,
    loading: topROILoading,
  } = useApi(getReskillingHighestROI, [8], []);

  const criticalCount = useMemo(
    () =>
      (skills ?? []).filter(
        (s) => (s.automation_threat_level ?? s.threat_level) === 'CRITICAL'
      ).length,
    [skills]
  );

  const jobsAtRisk = useMemo(() => {
    const total =
      workforceImpact?.total_jobs_at_risk_usa ?? workforceImpact?.total_jobs_at_risk;
    if (total) return formatJobCount(total);
    return '—';
  }, [workforceImpact]);

  return (
    <div className="bg-gray-50 min-h-screen p-6 space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Skills Intelligence</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Skill decay forecasts, reskilling ROI pathways, and workforce displacement analytics
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Jobs at Risk (USA)"
          value={skillsLoading || wfLoading ? '…' : jobsAtRisk}
          subtitle="Automation-driven displacement"
          icon={Users}
          color="amber"
        />
        <MetricCard
          title="Reskilling Market"
          value="$94B"
          subtitle="Global opportunity by 2030"
          icon={TrendingDown}
          color="emerald"
        />
        <MetricCard
          title="Critical Skills"
          value={skillsLoading ? '…' : String(criticalCount)}
          subtitle="CRITICAL threat level skills"
          icon={Brain}
          color="red"
        />
      </div>

      {/* Tabs */}
      <Tabs defaultValue="decay" className="space-y-4">
        <TabsList className="bg-white border rounded-lg p-1 w-full sm:w-auto">
          <TabsTrigger
            value="decay"
            className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4"
          >
            Skills Decay
          </TabsTrigger>
          <TabsTrigger
            value="reskilling"
            className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4"
          >
            Reskilling Pathways
          </TabsTrigger>
          <TabsTrigger
            value="workforce"
            className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4"
          >
            Workforce Impact
          </TabsTrigger>
        </TabsList>

        <TabsContent value="decay">
          <SkillsDecayTab
            skills={skills}
            loading={skillsLoading}
            error={skillsError}
            refetch={skillsRefetch}
          />
        </TabsContent>

        <TabsContent value="reskilling">
          <ReskillingTab
            pathways={pathways}
            topROI={topROI}
            loading={pathwaysLoading || topROILoading}
            error={pathwaysError}
            refetch={pathwaysRefetch}
          />
        </TabsContent>

        <TabsContent value="workforce">
          <WorkforceImpactTab
            skills={skills}
            workforceImpact={workforceImpact}
            loading={skillsLoading || wfLoading}
            error={skillsError ?? wfError}
            refetch={() => {
              skillsRefetch();
              wfRefetch();
            }}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
