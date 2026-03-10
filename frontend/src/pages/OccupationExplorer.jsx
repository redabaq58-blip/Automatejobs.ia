import { useState, useEffect, useRef, useMemo } from 'react';
import { Search, ExternalLink, ChevronUp, ChevronDown, Users, Layers } from 'lucide-react';

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import {
  Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription,
} from '@/components/ui/sheet';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

import { ScoreBar, TierBadge, ScoreBadge, getScoreColor } from '@/components/shared/ScoreBadge';
import { LoadingTable, ErrorState } from '@/components/shared/LoadingState';
import { ImpactBadge } from '@/components/shared/ComplianceBadge';

import { getOccupations, getTasksForOccupation, getOccupationSummary } from '@/lib/api';

// ── Helpers ───────────────────────────────────────────────────────────────────

const JURISDICTIONS = [
  { value: 'USA-Federal', label: '🇺🇸 USA Federal' },
  { value: 'Canada', label: '🇨🇦 Canada' },
  { value: 'EU', label: '🇪🇺 European Union' },
  { value: 'Quebec-Law25', label: '🇨🇦 Quebec Law 25' },
];

const TIER_ORDER = ['None', 'Low', 'Medium', 'High', 'Full'];

const tierBarColor = {
  None: 'bg-red-400',
  Low: 'bg-orange-400',
  Medium: 'bg-amber-400',
  High: 'bg-blue-400',
  Full: 'bg-emerald-500',
};

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}

function SortIcon({ column, sortBy, sortDir }) {
  if (sortBy !== column) return <ChevronUp className="h-3 w-3 text-gray-300 ml-0.5" />;
  return sortDir === 'asc'
    ? <ChevronUp className="h-3 w-3 text-violet-600 ml-0.5" />
    : <ChevronDown className="h-3 w-3 text-violet-600 ml-0.5" />;
}

// ── Tier Distribution Bar ─────────────────────────────────────────────────────
function TierDistributionBar({ distribution }) {
  if (!distribution || Object.keys(distribution).length === 0) return null;
  const total = Object.values(distribution).reduce((a, b) => a + b, 0);
  if (total === 0) return null;

  return (
    <div className="space-y-1.5">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Tier Distribution</p>
      <div className="flex h-4 rounded-full overflow-hidden w-full">
        {TIER_ORDER.map((tier) => {
          const count = distribution[tier] ?? 0;
          const pct = (count / total) * 100;
          if (pct === 0) return null;
          return (
            <div
              key={tier}
              className={`${tierBarColor[tier] || 'bg-gray-300'} transition-all`}
              style={{ width: `${pct}%` }}
              title={`${tier}: ${count} tasks (${pct.toFixed(0)}%)`}
            />
          );
        })}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {TIER_ORDER.map((tier) => {
          const count = distribution[tier] ?? 0;
          if (count === 0) return null;
          return (
            <span key={tier} className="flex items-center gap-1 text-xs text-muted-foreground">
              <span className={`inline-block h-2 w-2 rounded-full ${tierBarColor[tier]}`} />
              {tier} ({count})
            </span>
          );
        })}
      </div>
    </div>
  );
}

// ── Occupation Detail Sheet ───────────────────────────────────────────────────
function OccupationSheet({ occupation, jurisdiction, open, onClose }) {
  const [tasks, setTasks] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loadingTasks, setLoadingTasks] = useState(false);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [errorTasks, setErrorTasks] = useState(null);

  useEffect(() => {
    if (!occupation || !open) return;

    let cancelled = false;
    const id = occupation.occupation_id || occupation.id;

    // Load summary
    setLoadingSummary(true);
    getOccupationSummary(id, jurisdiction)
      .then((res) => { if (!cancelled) setSummary(res); })
      .catch(() => { if (!cancelled) setSummary(null); })
      .finally(() => { if (!cancelled) setLoadingSummary(false); });

    // Load tasks
    setLoadingTasks(true);
    setErrorTasks(null);
    getTasksForOccupation(id, jurisdiction)
      .then((res) => {
        if (cancelled) return;
        const arr = Array.isArray(res) ? res : res?.tasks ?? [];
        const sorted = [...arr].sort(
          (a, b) => (b.automation_score ?? 0) - (a.automation_score ?? 0)
        );
        setTasks(sorted);
      })
      .catch((err) => {
        if (!cancelled) setErrorTasks(err?.response?.data?.detail || err.message || 'Failed to load tasks');
      })
      .finally(() => { if (!cancelled) setLoadingTasks(false); });

    return () => { cancelled = true; };
  }, [occupation, open, jurisdiction]);

  const onetCode = occupation?.onet_code || occupation?.onet_soc_code || '—';
  const nocCode = occupation?.noc_code || null;
  const avgScore = summary?.avg_automation_score ?? occupation?.avg_automation_score ?? null;
  const totalTasks = summary?.total_tasks ?? occupation?.total_tasks ?? tasks.length ?? null;
  const blockedTasks = summary?.blocked_tasks ?? summary?.compliance_blocked ?? null;
  const tierDist = summary?.tier_distribution ?? summary?.tiers ?? null;

  return (
    <Sheet open={open} onOpenChange={(v) => { if (!v) onClose(); }}>
      <SheetContent side="right" className="w-full sm:max-w-2xl p-0 flex flex-col">
        {/* Header */}
        <SheetHeader className="px-6 pt-6 pb-4 border-b border-border">
          <SheetTitle className="text-lg font-bold text-foreground leading-snug">
            {occupation?.occupation_title || occupation?.title || '—'}
          </SheetTitle>
          <SheetDescription asChild>
            <div className="flex flex-wrap items-center gap-2 mt-1">
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono bg-gray-100 text-gray-700 border border-gray-200">
                O*NET {onetCode}
              </span>
              {nocCode && (
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono bg-blue-50 text-blue-700 border border-blue-200">
                  NOC {nocCode}
                </span>
              )}
              {occupation?.industry && (
                <Badge variant="secondary" className="text-xs">
                  {occupation.industry}
                </Badge>
              )}
            </div>
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="flex-1 overflow-y-auto">
          <div className="px-6 py-5 space-y-6">

            {/* Automation Summary */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-foreground">Automation Summary</h3>

              {loadingSummary ? (
                <div className="flex gap-3">
                  <Skeleton className="h-16 flex-1 rounded-lg" />
                  <Skeleton className="h-16 flex-1 rounded-lg" />
                  <Skeleton className="h-16 flex-1 rounded-lg" />
                </div>
              ) : (
                <div className="grid grid-cols-3 gap-3">
                  <div className="rounded-lg border border-border bg-gray-50 p-3 text-center">
                    <p className={`text-2xl font-bold ${avgScore != null ? getScoreColor(avgScore) : 'text-foreground'}`}>
                      {avgScore != null ? Math.round(avgScore) : '—'}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">Avg Score</p>
                  </div>
                  <div className="rounded-lg border border-border bg-gray-50 p-3 text-center">
                    <p className="text-2xl font-bold text-foreground">
                      {totalTasks ?? '—'}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">Total Tasks</p>
                  </div>
                  <div className="rounded-lg border border-border bg-gray-50 p-3 text-center">
                    <p className="text-2xl font-bold text-red-600">
                      {blockedTasks ?? '—'}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">Blocked Tasks</p>
                  </div>
                </div>
              )}

              {!loadingSummary && tierDist && (
                <TierDistributionBar distribution={tierDist} />
              )}
            </div>

            <Separator />

            {/* Tasks Section */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Tasks</h3>
                {!loadingTasks && tasks.length > 0 && (
                  <span className="text-xs text-muted-foreground">{tasks.length} tasks · sorted by score</span>
                )}
              </div>

              {loadingTasks ? (
                <LoadingTable rows={6} cols={4} />
              ) : errorTasks ? (
                <ErrorState error={errorTasks} />
              ) : tasks.length === 0 ? (
                <p className="text-sm text-muted-foreground py-4 text-center">No tasks found for this jurisdiction.</p>
              ) : (
                <div className="overflow-x-auto -mx-6 px-6">
                  <table className="w-full text-xs min-w-[540px]">
                    <thead>
                      <tr className="border-b border-border">
                        <th className="text-left py-2 pr-3 text-xs font-semibold text-muted-foreground">Task</th>
                        <th className="text-left py-2 pr-3 text-xs font-semibold text-muted-foreground w-28">Score</th>
                        <th className="text-left py-2 pr-3 text-xs font-semibold text-muted-foreground w-20">Tier</th>
                        <th className="text-left py-2 pr-3 text-xs font-semibold text-muted-foreground w-16">HITL</th>
                        <th className="text-left py-2 text-xs font-semibold text-muted-foreground w-20">EU Risk</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tasks.map((task, i) => {
                        const score = task.automation_score ?? task.score ?? 0;
                        const hitl = task.human_in_loop ?? task.hitl ?? task.requires_human;
                        const euRisk = task.eu_risk_level ?? task.eu_risk ?? task.risk_level;
                        return (
                          <tr key={task.task_id || i} className="border-b border-border/40 hover:bg-gray-50 transition-colors">
                            <td className="py-2 pr-3 max-w-[220px]">
                              <span className="block leading-snug text-foreground line-clamp-2">
                                {task.task_description || task.description || task.task || '—'}
                              </span>
                            </td>
                            <td className="py-2 pr-3">
                              <ScoreBar score={score} />
                            </td>
                            <td className="py-2 pr-3">
                              <TierBadge tier={task.automation_tier || task.tier || 'None'} />
                            </td>
                            <td className="py-2 pr-3">
                              {hitl != null ? (
                                <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium border ${
                                  hitl
                                    ? 'bg-amber-50 text-amber-700 border-amber-200'
                                    : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                }`}>
                                  {hitl ? 'Yes' : 'No'}
                                </span>
                              ) : (
                                <span className="text-muted-foreground">—</span>
                              )}
                            </td>
                            <td className="py-2">
                              {euRisk ? (
                                <ImpactBadge impact={euRisk} />
                              ) : (
                                <span className="text-muted-foreground">—</span>
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
          </div>
        </ScrollArea>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-border bg-gray-50/50 shrink-0">
          <a
            href="/build/wizard"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-violet-600 hover:text-violet-700 transition-colors"
          >
            Build Automation
            <ExternalLink className="h-4 w-4" />
          </a>
        </div>
      </SheetContent>
    </Sheet>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function OccupationExplorer() {
  const [searchQuery, setSearchQuery] = useState('');
  const [industryFilter, setIndustryFilter] = useState('all');
  const [jurisdictionFilter, setJurisdictionFilter] = useState('USA-Federal');
  const [selectedOccupation, setSelectedOccupation] = useState(null);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [sortBy, setSortBy] = useState('avg_automation_score');
  const [sortDir, setSortDir] = useState('desc');

  const [occupations, setOccupations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const debouncedSearch = useDebounce(searchQuery, 500);
  const abortRef = useRef(null);

  // ── Load occupations ──
  useEffect(() => {
    if (abortRef.current) abortRef.current = false;
    abortRef.current = true;
    const token = abortRef.current;

    setLoading(true);
    setError(null);

    const industry = industryFilter === 'all' ? '' : industryFilter;
    getOccupations(debouncedSearch, industry, '', 100)
      .then((res) => {
        if (!token) return;
        const arr = Array.isArray(res) ? res : res?.occupations ?? [];
        setOccupations(arr);
      })
      .catch((err) => {
        if (!token) return;
        setError(err?.response?.data?.detail || err.message || 'Failed to load occupations');
      })
      .finally(() => { if (token) setLoading(false); });
  }, [debouncedSearch, industryFilter]);

  // ── Derive unique industries ──
  const industries = useMemo(() => {
    const set = new Set();
    occupations.forEach((o) => {
      const ind = o.industry || o.industry_name;
      if (ind) set.add(ind);
    });
    return Array.from(set).sort();
  }, [occupations]);

  // ── Filter by jurisdiction (client-side label only) ──
  const filtered = useMemo(() => {
    return occupations; // server already filters by query/industry
  }, [occupations]);

  // ── Sort ──
  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      let av = a[sortBy] ?? 0;
      let bv = b[sortBy] ?? 0;
      if (typeof av === 'string') av = av.toLowerCase();
      if (typeof bv === 'string') bv = bv.toLowerCase();
      if (av < bv) return sortDir === 'asc' ? -1 : 1;
      if (av > bv) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });
  }, [filtered, sortBy, sortDir]);

  function handleSort(col) {
    if (sortBy === col) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortBy(col);
      setSortDir('desc');
    }
  }

  function handleRowClick(occ) {
    setSelectedOccupation(occ);
    setSheetOpen(true);
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-5">
      {/* ── Page header ── */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Occupation Explorer</h1>
        <p className="text-sm text-muted-foreground mt-0.5">
          Browse occupations, view automation scores, and explore task-level detail
        </p>
      </div>

      {/* ── Search & Filter Bar ── */}
      <div className="bg-white border border-border rounded-xl p-4 shadow-sm">
        <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search occupations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 bg-gray-50 border-border focus:bg-white"
            />
          </div>

          {/* Industry filter */}
          <Select value={industryFilter} onValueChange={setIndustryFilter}>
            <SelectTrigger className="w-full sm:w-48 bg-gray-50 border-border">
              <SelectValue placeholder="All Industries" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Industries</SelectItem>
              {industries.map((ind) => (
                <SelectItem key={ind} value={ind}>{ind}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Jurisdiction filter */}
          <Select value={jurisdictionFilter} onValueChange={setJurisdictionFilter}>
            <SelectTrigger className="w-full sm:w-48 bg-gray-50 border-border">
              <SelectValue placeholder="Jurisdiction" />
            </SelectTrigger>
            <SelectContent>
              {JURISDICTIONS.map((j) => (
                <SelectItem key={j.value} value={j.value}>{j.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Result count */}
          <div className="shrink-0">
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-violet-100 text-violet-700 border border-violet-200">
              <Users className="h-3 w-3" />
              {loading ? '…' : sorted.length} results
            </span>
          </div>
        </div>
      </div>

      {/* ── Occupations Table ── */}
      <div className="bg-white border border-border rounded-xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-6">
            <LoadingTable rows={8} cols={5} />
          </div>
        ) : error ? (
          <div className="p-6">
            <ErrorState error={error} />
          </div>
        ) : sorted.length === 0 ? (
          <div className="py-16 text-center">
            <div className="h-12 w-12 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
              <Layers className="h-6 w-6 text-gray-400" />
            </div>
            <p className="text-sm font-medium text-foreground">No occupations found</p>
            <p className="text-xs text-muted-foreground mt-1">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="bg-gray-50/60 hover:bg-gray-50/60">
                  <TableHead
                    className="cursor-pointer select-none hover:text-foreground transition-colors font-semibold"
                    onClick={() => handleSort('occupation_title')}
                  >
                    <span className="inline-flex items-center">
                      Title
                      <SortIcon column="occupation_title" sortBy={sortBy} sortDir={sortDir} />
                    </span>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:text-foreground transition-colors font-semibold"
                    onClick={() => handleSort('industry')}
                  >
                    <span className="inline-flex items-center">
                      Industry
                      <SortIcon column="industry" sortBy={sortBy} sortDir={sortDir} />
                    </span>
                  </TableHead>
                  <TableHead className="font-semibold">O*NET Code</TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:text-foreground transition-colors font-semibold w-40"
                    onClick={() => handleSort('avg_automation_score')}
                  >
                    <span className="inline-flex items-center">
                      Avg Score
                      <SortIcon column="avg_automation_score" sortBy={sortBy} sortDir={sortDir} />
                    </span>
                  </TableHead>
                  <TableHead
                    className="cursor-pointer select-none hover:text-foreground transition-colors font-semibold"
                    onClick={() => handleSort('total_tasks')}
                  >
                    <span className="inline-flex items-center">
                      Tasks
                      <SortIcon column="total_tasks" sortBy={sortBy} sortDir={sortDir} />
                    </span>
                  </TableHead>
                  <TableHead className="text-right font-semibold">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sorted.map((occ) => {
                  const score = occ.avg_automation_score ?? occ.automation_score ?? 0;
                  const onetCode = occ.onet_code || occ.onet_soc_code || '—';
                  const taskCount = occ.total_tasks ?? occ.task_count ?? '—';
                  const industry = occ.industry || occ.industry_name || '—';

                  return (
                    <TableRow
                      key={occ.occupation_id || occ.id}
                      className="cursor-pointer hover:bg-gray-50 transition-colors"
                      onClick={() => handleRowClick(occ)}
                    >
                      <TableCell className="font-medium text-foreground max-w-[220px]">
                        <span className="block truncate">
                          {occ.occupation_title || occ.title || '—'}
                        </span>
                      </TableCell>
                      <TableCell className="text-muted-foreground max-w-[160px]">
                        <span className="block truncate">{industry}</span>
                      </TableCell>
                      <TableCell>
                        <span className="font-mono text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded border border-gray-200">
                          {onetCode}
                        </span>
                      </TableCell>
                      <TableCell>
                        <ScoreBar score={score} className="min-w-[100px]" />
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {taskCount}
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-violet-600 hover:text-violet-700 hover:bg-violet-50 text-xs font-semibold"
                          onClick={(e) => { e.stopPropagation(); handleRowClick(occ); }}
                        >
                          Explore
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        )}
      </div>

      {/* ── Occupation Detail Sheet ── */}
      <OccupationSheet
        occupation={selectedOccupation}
        jurisdiction={jurisdictionFilter}
        open={sheetOpen}
        onClose={() => setSheetOpen(false)}
      />
    </div>
  );
}
