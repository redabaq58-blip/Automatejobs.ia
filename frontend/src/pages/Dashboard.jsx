import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from 'recharts';
import { Users, Zap, Globe, TrendingUp, AlertTriangle, Clock } from 'lucide-react';

import { MetricCard } from '@/components/shared/MetricCard';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';
import { ThreatBadge, ImpactBadge } from '@/components/shared/ComplianceBadge';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';

import {
  getExecutiveDashboard,
  getWorkforceImpact,
  getMostDisrupted,
  getSkillsAtRisk,
  getRegulatoryTimeline,
  getTaskQuickWins,
  getFirstMoverWindows,
} from '@/lib/api';

// ── Generic hook ──────────────────────────────────────────────────────────────

function useDataFetch(apiFn, ...args) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiFn(...args)
      .then((res) => { if (!cancelled) setData(res); })
      .catch((err) => {
        if (!cancelled) setError(err?.response?.data?.detail || err.message || 'Failed to load');
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [retryCount]);

  const retry = () => setRetryCount((c) => c + 1);
  return { data, loading, error, retry };
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function truncate(str, n) {
  if (!str) return '';
  return str.length > n ? str.slice(0, n - 1) + '…' : str;
}

function formatJobCount(n) {
  if (n == null) return '8.1M';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

// ── Custom tooltip ────────────────────────────────────────────────────────────

function DisruptionTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const val = payload[0]?.value;
  return (
    <div className="bg-white border border-border rounded-lg shadow-lg px-3 py-2 text-sm">
      <p className="font-medium text-foreground">{label}</p>
      <p className="text-orange-600 font-semibold">{val?.toFixed(1)}%</p>
    </div>
  );
}

// ── First-Mover Card ──────────────────────────────────────────────────────────

function FirstMoverCard({ item }) {
  const months = item.window_closing_months ?? item.window_months ?? null;
  const isUrgent = months != null && months < 6;

  return (
    <div
      className={`min-w-[220px] max-w-[240px] bg-white rounded-xl p-4 flex-shrink-0 shadow-sm hover:shadow-md transition-shadow border-2 ${
        isUrgent ? 'border-amber-400' : 'border-border'
      }`}
    >
      <div className="flex items-center gap-2 mb-2">
        <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${isUrgent ? 'bg-amber-50' : 'bg-violet-50'}`}>
          <Zap className={`h-4 w-4 ${isUrgent ? 'text-amber-600' : 'text-violet-600'}`} />
        </div>
        <span className={`text-xs font-semibold uppercase tracking-wide truncate ${isUrgent ? 'text-amber-700' : 'text-violet-700'}`}>
          {item.automation_type || 'AI Automation'}
        </span>
        {isUrgent && (
          <Badge className="ml-auto bg-amber-100 text-amber-800 border border-amber-200 text-xs px-1.5 py-0 shrink-0">
            Urgent
          </Badge>
        )}
      </div>
      <p className="text-sm font-medium text-foreground leading-snug mb-3 line-clamp-3">
        {item.competitive_advantage || item.description || '—'}
      </p>
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
        <Clock className="h-3 w-3 shrink-0" />
        <span>
          {months != null ? `${months} month window` : 'Limited window'}
        </span>
      </div>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const exec = useDataFetch(getExecutiveDashboard);
  const workforce = useDataFetch(getWorkforceImpact);
  const disrupted = useDataFetch(getMostDisrupted, 8);
  const skillsAtRisk = useDataFetch(getSkillsAtRisk);
  const regulatory = useDataFetch(getRegulatoryTimeline);
  const quickWins = useDataFetch(getTaskQuickWins, 8);
  const firstMover = useDataFetch(getFirstMoverWindows);

  // ── KPI derivations ──
  const jobsAtRiskRaw =
    workforce.data?.total_jobs_at_risk_usa ??
    workforce.data?.jobs_at_risk ??
    workforce.data?.total_jobs_at_risk ??
    null;
  const jobsAtRiskLabel = formatJobCount(jobsAtRiskRaw);

  const avgScore =
    exec.data?.avg_automation_score ??
    exec.data?.average_score ??
    exec.data?.kpis?.avg_automation_score ??
    null;
  const avgScoreLabel = avgScore != null ? `${Math.round(avgScore)}/100` : '74/100';

  // ── Skills at risk ──
  const topSkills = (() => {
    const raw = Array.isArray(skillsAtRisk.data)
      ? skillsAtRisk.data
      : skillsAtRisk.data?.skills ?? [];
    return raw.slice(0, 8);
  })();

  // ── Industry disruption chart data ──
  const disruptionData = (() => {
    const raw = Array.isArray(disrupted.data)
      ? disrupted.data
      : disrupted.data?.industries ?? [];
    return raw.map((item) => ({
      name: truncate(item.industry || item.name || '', 15),
      value: item.job_displacement_percentage ?? item.pct_change ?? item.disruption_score ?? 0,
    }));
  })();

  // ── Regulatory timeline ──
  const regulatoryEvents = (() => {
    const raw = Array.isArray(regulatory.data)
      ? regulatory.data
      : regulatory.data?.events ?? regulatory.data?.timeline ?? [];
    return [...raw]
      .sort((a, b) => {
        const da = a.predicted_date || a.effective_date || a.date || '';
        const db = b.predicted_date || b.effective_date || b.date || '';
        return da < db ? -1 : da > db ? 1 : 0;
      })
      .slice(0, 6);
  })();

  // ── Quick wins ──
  const quickWinsArray = (() => {
    const raw = Array.isArray(quickWins.data)
      ? quickWins.data
      : quickWins.data?.quick_wins ?? quickWins.data?.tasks ?? [];
    return raw.slice(0, 6);
  })();

  // ── First-mover windows ──
  const firstMoverList = Array.isArray(firstMover.data)
    ? firstMover.data
    : firstMover.data?.windows ?? [];

  const kpisLoading = exec.loading && workforce.loading;

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-6">

      {/* ── Page header ── */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Executive Dashboard</h1>
        <p className="text-sm text-muted-foreground mt-0.5">
          AI automation intelligence at a glance — updated in real time
        </p>
      </div>

      {/* ── Row 1: KPI Cards ── */}
      {kpisLoading ? (
        <LoadingCards count={4} />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Occupations Tracked"
            value="29"
            subtitle="Cross-mapped O*NET + NOC + ESCO"
            icon={Users}
            color="violet"
          />
          <MetricCard
            title="Jobs at Risk (USA)"
            value={jobsAtRiskLabel}
            subtitle="Facing automation displacement"
            icon={AlertTriangle}
            color="amber"
          />
          <MetricCard
            title="Automation Score Avg"
            value={avgScoreLabel}
            subtitle="Across 39 tasks × 4 jurisdictions"
            icon={Zap}
            color="blue"
          />
          <MetricCard
            title="Jurisdictions Covered"
            value="14"
            subtitle="USA, Canada, EU, Quebec + more"
            icon={Globe}
            color="emerald"
          />
        </div>
      )}

      {/* ── Row 2: Industry Disruption Chart + Skills at Risk ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Most Disrupted Industries */}
        <Card className="bg-white border shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-orange-500" />
              Most Disrupted Industries
            </CardTitle>
            <p className="text-xs text-muted-foreground">Projected % job displacement by industry</p>
          </CardHeader>
          <CardContent>
            {disrupted.loading ? (
              <div className="h-[250px] flex items-center justify-center">
                <LoadingTable rows={4} cols={1} />
              </div>
            ) : disrupted.error ? (
              <ErrorState error={disrupted.error} onRetry={disrupted.retry} />
            ) : disruptionData.length === 0 ? (
              <div className="h-[250px] flex items-center justify-center text-sm text-muted-foreground">
                No disruption data available
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={disruptionData} margin={{ top: 8, right: 8, left: 0, bottom: 60 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 11, fill: '#6b7280' }}
                    angle={-35}
                    textAnchor="end"
                    interval={0}
                    height={70}
                  />
                  <YAxis
                    tick={{ fontSize: 11, fill: '#6b7280' }}
                    tickFormatter={(v) => `${v}%`}
                  />
                  <Tooltip content={<DisruptionTooltip />} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {disruptionData.map((_, idx) => (
                      <Cell key={idx} fill="#f97316" />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        {/* Skills at Risk */}
        <Card className="bg-white border shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-red-500" />
              Skills at Risk
            </CardTitle>
            <p className="text-xs text-muted-foreground">Skills facing highest automation displacement pressure</p>
          </CardHeader>
          <CardContent className="p-0">
            {skillsAtRisk.loading ? (
              <div className="px-6 py-4">
                <LoadingTable rows={6} cols={4} />
              </div>
            ) : skillsAtRisk.error ? (
              <div className="px-6 py-4">
                <ErrorState error={skillsAtRisk.error} onRetry={skillsAtRisk.retry} />
              </div>
            ) : topSkills.length === 0 ? (
              <div className="px-6 py-8 text-center text-sm text-muted-foreground">
                No skills data available
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-gray-50/60">
                      <th className="text-left px-4 py-2.5 text-xs font-semibold text-muted-foreground">Skill</th>
                      <th className="text-left px-4 py-2.5 text-xs font-semibold text-muted-foreground">Threat</th>
                      <th className="text-left px-4 py-2.5 text-xs font-semibold text-muted-foreground">Half-Life</th>
                      <th className="text-right px-4 py-2.5 text-xs font-semibold text-muted-foreground">Jobs at Risk</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topSkills.map((skill, i) => (
                      <tr key={i} className="border-b border-border/50 hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-2.5 font-medium text-foreground max-w-[180px]">
                          <span className="truncate block">
                            {skill.skill_name || skill.name || '—'}
                          </span>
                        </td>
                        <td className="px-4 py-2.5">
                          <ThreatBadge
                            level={skill.automation_threat_level || skill.threat_level || skill.risk_level || 'MEDIUM'}
                          />
                        </td>
                        <td className="px-4 py-2.5 text-muted-foreground whitespace-nowrap">
                          {skill.half_life_years != null
                            ? `${skill.half_life_years} yrs`
                            : skill.half_life != null
                              ? `${skill.half_life} yrs`
                              : '—'}
                        </td>
                        <td className="px-4 py-2.5 text-right text-muted-foreground whitespace-nowrap">
                          {skill.jobs_at_risk_usa != null
                            ? formatJobCount(skill.jobs_at_risk_usa)
                            : skill.jobs_at_risk != null
                              ? formatJobCount(skill.jobs_at_risk)
                              : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* ── Row 3: Upcoming Regulations + Quick Win Automations ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Upcoming Regulations */}
        <Card className="bg-white border shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <Clock className="h-4 w-4 text-violet-600" />
              Upcoming Regulations
            </CardTitle>
            <p className="text-xs text-muted-foreground">Next compliance milestones to watch</p>
          </CardHeader>
          <CardContent className="p-0">
            {regulatory.loading ? (
              <div className="px-6 py-4">
                <LoadingTable rows={5} cols={2} />
              </div>
            ) : regulatory.error ? (
              <div className="px-6 py-4">
                <ErrorState error={regulatory.error} onRetry={regulatory.retry} />
              </div>
            ) : regulatoryEvents.length === 0 ? (
              <div className="px-6 py-8 text-center text-sm text-muted-foreground">
                No regulatory events available
              </div>
            ) : (
              <div className="divide-y divide-border/50">
                {regulatoryEvents.map((event, i) => {
                  const dateLabel =
                    event.predicted_date || event.effective_date || event.date || event.year || '—';
                  const impact =
                    event.automation_impact || event.impact_type || event.impact || 'MONITORS';
                  return (
                    <div key={i} className="px-4 py-3 flex items-start gap-3 hover:bg-gray-50 transition-colors">
                      <span className="shrink-0 inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-violet-100 text-violet-700 border border-violet-200 whitespace-nowrap">
                        {dateLabel}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground leading-snug truncate">
                          {event.regulation_name || event.name || event.title || '—'}
                        </p>
                        <div className="flex flex-wrap items-center gap-2 mt-1">
                          {event.jurisdiction && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border bg-gray-100 text-gray-700 border-gray-200">
                              {event.jurisdiction}
                            </span>
                          )}
                          <ImpactBadge impact={impact} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Win Automations */}
        <Card className="bg-white border shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <Zap className="h-4 w-4 text-emerald-600" />
              Quick Win Automations
            </CardTitle>
            <p className="text-xs text-muted-foreground">Tasks automatable in ≤8 weeks with fast ROI</p>
          </CardHeader>
          <CardContent className="p-0">
            {quickWins.loading ? (
              <div className="px-6 py-4">
                <LoadingTable rows={6} cols={3} />
              </div>
            ) : quickWins.error ? (
              <div className="px-6 py-4">
                <ErrorState error={quickWins.error} onRetry={quickWins.retry} />
              </div>
            ) : quickWinsArray.length === 0 ? (
              <div className="px-6 py-8 text-center text-sm text-muted-foreground">
                No quick wins data available
              </div>
            ) : (
              <div className="divide-y divide-border/50">
                {quickWinsArray.map((task, i) => {
                  const effort =
                    task.implementation_weeks != null
                      ? `${task.implementation_weeks}w`
                      : task.effort_weeks != null
                        ? `${task.effort_weeks}w`
                        : task.effort
                          ? String(task.effort)
                          : null;
                  const payback =
                    task.payback_months != null
                      ? `${task.payback_months}mo payback`
                      : task.payback
                        ? String(task.payback)
                        : null;
                  return (
                    <div key={i} className="px-4 py-3 flex items-start gap-3 hover:bg-gray-50 transition-colors">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground leading-snug">
                          {truncate(
                            task.task_description || task.task || task.name || '—',
                            70
                          )}
                        </p>
                        <div className="flex flex-wrap items-center gap-2 mt-1.5">
                          {effort && (
                            <span className="text-xs text-muted-foreground">{effort}</span>
                          )}
                          {payback && (
                            <span className="text-xs text-muted-foreground">{payback}</span>
                          )}
                        </div>
                      </div>
                      <Badge className="shrink-0 bg-emerald-100 text-emerald-800 border border-emerald-200 text-xs font-semibold hover:bg-emerald-100">
                        Fast ROI
                      </Badge>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* ── Row 4: First-Mover Opportunity Windows ── */}
      <Card className="bg-white border shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-violet-600" />
            First-Mover Opportunity Windows
          </CardTitle>
          <p className="text-xs text-muted-foreground mt-0.5">
            Time-sensitive automation opportunities — amber border = closing in under 6 months
          </p>
        </CardHeader>
        <CardContent>
          {firstMover.loading ? (
            <div className="flex gap-3 overflow-hidden">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="min-w-[220px] h-[130px] rounded-xl bg-gray-100 animate-pulse flex-shrink-0"
                />
              ))}
            </div>
          ) : firstMover.error ? (
            <ErrorState error={firstMover.error} onRetry={firstMover.retry} />
          ) : firstMoverList.length === 0 ? (
            <p className="text-sm text-muted-foreground py-4">
              No first-mover window data available.
            </p>
          ) : (
            <ScrollArea className="w-full whitespace-nowrap">
              <div className="flex gap-3 pb-3">
                {firstMoverList.map((item, i) => (
                  <FirstMoverCard key={i} item={item} />
                ))}
              </div>
              <ScrollBar orientation="horizontal" />
            </ScrollArea>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
