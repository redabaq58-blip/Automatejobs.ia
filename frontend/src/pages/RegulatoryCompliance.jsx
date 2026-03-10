import { useMemo } from 'react';
import { Scale, Globe, Shield, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from '@/components/ui/accordion';
import { MetricCard } from '@/components/shared/MetricCard';
import { JurisdictionBadge, ImpactBadge } from '@/components/shared/ComplianceBadge';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';
import { useApi } from '@/hooks/useApi';
import {
  getRegulatoryTimeline,
  getRegulatoryAll,
  getComplianceBlocked,
} from '@/lib/api';

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function formatMonthYear(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;
  return `${MONTH_NAMES[d.getMonth()]} ${d.getFullYear()}`;
}

function getYear(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return null;
  return d.getFullYear();
}

function formatCost(n) {
  if (!n && n !== 0) return '—';
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

const JURISDICTION_FLAGS = {
  EU: '🇪🇺',
  'USA-Federal': '🇺🇸',
  USA: '🇺🇸',
  UK: '🇬🇧',
  Canada: '🇨🇦',
  'Quebec-Law25': '🇨🇦',
  Australia: '🇦🇺',
  China: '🇨🇳',
  Japan: '🇯🇵',
  Singapore: '🇸🇬',
  India: '🇮🇳',
  Brazil: '🇧🇷',
  Germany: '🇩🇪',
  France: '🇫🇷',
};

function getFlag(jurisdiction) {
  return JURISDICTION_FLAGS[jurisdiction] ?? '🏛️';
}

function euRiskBadge(level) {
  const config = {
    HIGH_RISK: 'bg-red-100 text-red-800 border-red-200',
    LIMITED_RISK: 'bg-amber-100 text-amber-800 border-amber-200',
    MINIMAL_RISK: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  }[level] ?? 'bg-gray-100 text-gray-700 border-gray-200';
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${config}`}>
      {level?.replace(/_/g, ' ') ?? '—'}
    </span>
  );
}

// ── Tab 1: Timeline 2026–2030 ──────────────────────────────────────────────

function TimelineTab({ timeline, loading, error, refetch }) {
  const grouped = useMemo(() => {
    if (!timeline?.length) return {};
    const sorted = [...timeline].sort((a, b) => {
      const da = new Date(a.predicted_date ?? a.effective_date ?? '');
      const db = new Date(b.predicted_date ?? b.effective_date ?? '');
      return da - db;
    });
    return sorted.reduce((acc, item) => {
      const year = getYear(item.predicted_date ?? item.effective_date) ?? 'Unknown';
      if (!acc[year]) acc[year] = [];
      acc[year].push(item);
      return acc;
    }, {});
  }, [timeline]);

  if (loading) return <LoadingCards count={4} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!timeline?.length)
    return <p className="text-sm text-muted-foreground py-8 text-center">No timeline data available.</p>;

  return (
    <div className="space-y-8">
      {Object.entries(grouped).map(([year, items]) => (
        <div key={year}>
          {/* Year divider */}
          <div className="flex items-center gap-3 mb-4">
            <div className="h-px flex-1 bg-gray-200" />
            <span className="text-sm font-bold text-violet-700 bg-violet-50 border border-violet-200 px-3 py-1 rounded-full">
              {year}
            </span>
            <div className="h-px flex-1 bg-gray-200" />
          </div>

          {/* Timeline items */}
          <div className="relative pl-8 space-y-4">
            <div className="absolute left-3 top-0 bottom-0 w-px bg-gray-200" />
            {items.map((item, idx) => {
              const dateKey = item.predicted_date ?? item.effective_date;
              const impact = item.automation_impact ?? item.impact;
              return (
                <div key={item.id ?? idx} className="relative">
                  {/* Dot */}
                  <div className="absolute -left-5 top-3 h-2.5 w-2.5 rounded-full bg-violet-500 border-2 border-white shadow" />

                  <Card className="border shadow-sm rounded-xl bg-white">
                    <CardContent className="p-4">
                      <div className="flex flex-wrap items-start gap-2 mb-2">
                        {/* Date chip */}
                        <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-violet-600 text-white shrink-0">
                          {formatMonthYear(dateKey)}
                        </span>
                        <JurisdictionBadge jurisdiction={item.jurisdiction} />
                        {impact && <ImpactBadge impact={impact} />}
                      </div>
                      <p className="font-semibold text-sm text-foreground">
                        {item.regulation_name ?? item.title ?? item.name ?? '—'}
                      </p>
                      {item.description && (
                        <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{item.description}</p>
                      )}
                      {item.compliance_cost_usd != null && (
                        <p className="text-xs text-muted-foreground mt-1">
                          Compliance cost: <span className="font-medium">{formatCost(item.compliance_cost_usd)}</span>
                        </p>
                      )}
                    </CardContent>
                  </Card>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Tab 2: By Jurisdiction ─────────────────────────────────────────────────

function ByJurisdictionTab({ regulatoryAll, loading, error, refetch }) {
  // regulatoryAll may be an array of items (each with a jurisdiction field)
  // or an object keyed by jurisdiction
  const jurisdictions = useMemo(() => {
    if (!regulatoryAll) return {};
    if (Array.isArray(regulatoryAll)) {
      return regulatoryAll.reduce((acc, item) => {
        const jur = item.jurisdiction ?? 'Unknown';
        if (!acc[jur]) acc[jur] = [];
        acc[jur].push(item);
        return acc;
      }, {});
    }
    // Already object
    return regulatoryAll;
  }, [regulatoryAll]);

  if (loading) return <LoadingCards count={6} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (!Object.keys(jurisdictions).length)
    return <p className="text-sm text-muted-foreground py-8 text-center">No jurisdiction data available.</p>;

  return (
    <Accordion type="multiple" className="space-y-2">
      {Object.entries(jurisdictions).map(([jur, items]) => (
        <AccordionItem
          key={jur}
          value={jur}
          className="border rounded-xl bg-white shadow-sm overflow-hidden"
        >
          <AccordionTrigger className="px-4 py-3 hover:no-underline hover:bg-gray-50 transition-colors">
            <div className="flex items-center gap-2">
              <span className="text-lg leading-none">{getFlag(jur)}</span>
              <span className="font-semibold text-sm text-foreground">{jur}</span>
              <span className="text-xs text-muted-foreground ml-1">
                ({Array.isArray(items) ? items.length : 0} regulations)
              </span>
            </div>
          </AccordionTrigger>
          <AccordionContent className="px-0 pb-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-t bg-gray-50 text-xs text-muted-foreground uppercase tracking-wide">
                    <th className="text-left px-4 py-2 font-medium">Regulation</th>
                    <th className="text-left px-4 py-2 font-medium">Date</th>
                    <th className="text-right px-4 py-2 font-medium">Compliance Cost</th>
                    <th className="text-left px-4 py-2 font-medium">Impact</th>
                  </tr>
                </thead>
                <tbody>
                  {(Array.isArray(items) ? items : []).map((reg, idx) => (
                    <tr key={reg.id ?? idx} className="border-t hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-2.5 font-medium text-foreground max-w-xs">
                        {reg.regulation_name ?? reg.title ?? reg.name ?? '—'}
                      </td>
                      <td className="px-4 py-2.5 text-muted-foreground whitespace-nowrap">
                        {formatMonthYear(reg.predicted_date ?? reg.effective_date)}
                      </td>
                      <td className="px-4 py-2.5 text-right tabular-nums">
                        {reg.compliance_cost_usd != null ? formatCost(reg.compliance_cost_usd) : '—'}
                      </td>
                      <td className="px-4 py-2.5">
                        {reg.automation_impact ?? reg.impact ? (
                          <ImpactBadge impact={reg.automation_impact ?? reg.impact} />
                        ) : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}

// ── Tab 3: EU Blocked Tasks ────────────────────────────────────────────────

function EUBlockedTab({ blocked, loading, error, refetch }) {
  if (loading) return <LoadingTable rows={6} cols={4} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  const tasks = Array.isArray(blocked) ? blocked : blocked?.tasks ?? blocked?.blocked_tasks ?? [];

  return (
    <div className="space-y-4">
      {/* Explanation banner */}
      <Card className="border border-red-200 bg-red-50 shadow-sm rounded-xl">
        <CardContent className="p-4 flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-red-600 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-semibold text-red-800">EU AI Act — Blocked Tasks</p>
            <p className="text-xs text-red-700 mt-1 leading-relaxed">
              These tasks are prohibited or restricted under the EU AI Act for fully automated
              decision-making. Human-in-the-loop (HITL) oversight is legally required. Deploying
              automation without compliance may result in fines up to €30M or 6% of global revenue.
            </p>
          </div>
        </CardContent>
      </Card>

      {tasks.length > 0 ? (
        <div className="rounded-xl border bg-white overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-gray-50 text-xs text-muted-foreground uppercase tracking-wide">
                  <th className="text-left px-4 py-3 font-medium">Task Description</th>
                  <th className="text-left px-4 py-3 font-medium">EU Risk Level</th>
                  <th className="text-left px-4 py-3 font-medium">HITL Required</th>
                  <th className="text-left px-4 py-3 font-medium">Legal Reference</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task, idx) => (
                  <tr key={task.id ?? idx} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 max-w-xs">
                      <p className="font-medium text-foreground">
                        {task.task_description ?? task.description ?? task.task ?? task.title ?? '—'}
                      </p>
                      {task.category && (
                        <p className="text-xs text-muted-foreground mt-0.5">{task.category}</p>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      {euRiskBadge(task.eu_risk_level ?? task.risk_level)}
                    </td>
                    <td className="px-4 py-3">
                      {task.hitl_required != null ? (
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${
                            task.hitl_required
                              ? 'bg-red-100 text-red-800 border-red-200'
                              : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                          }`}
                        >
                          {task.hitl_required ? 'Required' : 'Not Required'}
                        </span>
                      ) : '—'}
                    </td>
                    <td className="px-4 py-3 text-xs text-muted-foreground max-w-xs">
                      {task.legal_reference ?? task.article ?? task.reference ?? '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <p className="text-sm text-muted-foreground py-8 text-center">No EU blocked tasks data available.</p>
      )}
    </div>
  );
}

// ── Main Component ─────────────────────────────────────────────────────────

export default function RegulatoryCompliance() {
  const { data: timeline, loading: tlLoading, error: tlError, refetch: tlRefetch } = useApi(getRegulatoryTimeline, [], []);
  const { data: regulatoryAll, loading: raLoading, error: raError, refetch: raRefetch } = useApi(getRegulatoryAll, [], []);
  const { data: blocked, loading: blLoading, error: blError, refetch: blRefetch } = useApi(getComplianceBlocked, ['EU'], []);

  // KPI: jurisdictions count
  const jurisdictionCount = useMemo(() => {
    if (!regulatoryAll) return '—';
    if (Array.isArray(regulatoryAll)) {
      const jurs = new Set(regulatoryAll.map((r) => r.jurisdiction).filter(Boolean));
      return String(jurs.size || regulatoryAll.length);
    }
    return String(Object.keys(regulatoryAll).length);
  }, [regulatoryAll]);

  // KPI: upcoming in 2026
  const upcoming2026 = useMemo(() => {
    if (!timeline?.length) return '—';
    const count = timeline.filter((item) => {
      const year = getYear(item.predicted_date ?? item.effective_date);
      return year === 2026;
    }).length;
    return String(count);
  }, [timeline]);

  // KPI: EU blocked count
  const blockedCount = useMemo(() => {
    if (!blocked) return '—';
    const tasks = Array.isArray(blocked) ? blocked : blocked?.tasks ?? blocked?.blocked_tasks ?? [];
    return String(tasks.length);
  }, [blocked]);

  return (
    <div className="bg-gray-50 min-h-screen p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Regulatory Compliance</h1>
        <p className="text-muted-foreground text-sm mt-1">
          AI regulation timeline, jurisdictional requirements, and EU AI Act compliance
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Jurisdictions Tracked"
          value={jurisdictionCount}
          subtitle="Global regulatory coverage"
          icon={Globe}
          color="violet"
        />
        <MetricCard
          title="Upcoming in 2026"
          value={upcoming2026}
          subtitle="Regulations taking effect"
          icon={Scale}
          color="amber"
        />
        <MetricCard
          title="EU Blocked Tasks"
          value={blockedCount}
          subtitle="EU AI Act restrictions"
          icon={Shield}
          color="red"
        />
      </div>

      {/* Tabs */}
      <Tabs defaultValue="timeline" className="space-y-4">
        <TabsList className="bg-white border rounded-lg p-1">
          <TabsTrigger value="timeline" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            Timeline 2026–2030
          </TabsTrigger>
          <TabsTrigger value="jurisdiction" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            By Jurisdiction
          </TabsTrigger>
          <TabsTrigger value="eu" className="data-[state=active]:bg-violet-600 data-[state=active]:text-white rounded-md px-4">
            EU Blocked Tasks
          </TabsTrigger>
        </TabsList>

        <TabsContent value="timeline">
          <TimelineTab
            timeline={timeline}
            loading={tlLoading}
            error={tlError}
            refetch={tlRefetch}
          />
        </TabsContent>

        <TabsContent value="jurisdiction">
          <ByJurisdictionTab
            regulatoryAll={regulatoryAll}
            loading={raLoading}
            error={raError}
            refetch={raRefetch}
          />
        </TabsContent>

        <TabsContent value="eu">
          <EUBlockedTab
            blocked={blocked}
            loading={blLoading}
            error={blError}
            refetch={blRefetch}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
