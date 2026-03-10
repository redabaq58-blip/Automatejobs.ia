import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer,
} from 'recharts';
import {
  Calculator, TrendingUp, DollarSign, Clock,
  CheckCircle, AlertCircle, Loader2, Building2, Star,
} from 'lucide-react';
import { useApi, useApiLazy } from '@/hooks/useApi';
import { getROIBenchmarks, getRoiAnalysis, calculateCustomROI } from '@/lib/api';
import { LoadingCards, LoadingTable, ErrorState } from '@/components/shared/LoadingState';

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fmt$(val) {
  if (val == null || val === '') return '—';
  const n = Number(val);
  if (isNaN(n)) return '—';
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (Math.abs(n) >= 1_000) return `$${n.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
  return `$${n.toFixed(0)}`;
}

function fmtPct(val, multiplier = 1) {
  if (val == null) return '—';
  const n = Number(val) * multiplier;
  if (isNaN(n)) return '—';
  return `${n.toFixed(0)}%`;
}

function paybackClass(months) {
  const m = Number(months);
  if (m < 6) return 'bg-emerald-100 text-emerald-800 border-emerald-200';
  if (m <= 12) return 'bg-blue-100 text-blue-800 border-blue-200';
  return 'bg-amber-100 text-amber-800 border-amber-200';
}

function paybackCardAccent(months) {
  const m = Number(months);
  if (m < 6) return { border: 'border-emerald-200', badge: 'bg-emerald-100 text-emerald-800 border-emerald-200', dot: 'bg-emerald-500' };
  if (m <= 12) return { border: 'border-blue-200', badge: 'bg-blue-100 text-blue-800 border-blue-200', dot: 'bg-blue-500' };
  return { border: 'border-amber-200', badge: 'bg-amber-100 text-amber-800 border-amber-200', dot: 'bg-amber-500' };
}

// Build the 36-month cumulative savings array (month 0 through 36)
function buildCumulativeSavings(result) {
  if (!result) return [];
  const annualSavings = result.annual_savings ?? 0;
  const implCost = result.implementation_cost ?? 0;
  const ongoingAnnual = result.ongoing_annual_cost ?? 0;
  const monthlySavings = annualSavings / 12;
  const monthlyOngoing = ongoingAnnual / 12;
  const months = [0, 6, 12, 18, 24, 30, 36];
  return months.map((m) => ({
    month: m,
    savings: Math.round(monthlySavings * m - monthlyOngoing * m - implCost),
  }));
}

// Find approximate break-even month
function breakEvenMonth(result) {
  if (!result) return null;
  const annualSavings = result.annual_savings ?? 0;
  const implCost = result.implementation_cost ?? 0;
  const ongoingAnnual = result.ongoing_annual_cost ?? 0;
  const net = annualSavings - ongoingAnnual;
  if (net <= 0) return null;
  return Math.round((implCost / net) * 12);
}

// ─── Custom Tooltip ───────────────────────────────────────────────────────────

function SavingsTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const val = payload[0]?.value;
  return (
    <div className="bg-white border border-border rounded-lg shadow-lg px-3 py-2 text-sm">
      <p className="text-muted-foreground text-xs mb-1">Month {label}</p>
      <p className={`font-semibold ${val >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
        {fmt$(val)}
      </p>
    </div>
  );
}

// ─── Section 1 – Interactive Calculator ──────────────────────────────────────

function CalculatorSection() {
  const [form, setForm] = useState({
    annual_salary: 55000,
    automation_percentage: 40,
    implementation_cost: 8000,
    ongoing_annual_cost: 2400,
    jurisdiction: 'USA-Federal',
  });
  const [result, setResult] = useState(null);
  const { execute, loading, error } = useApiLazy(calculateCustomROI);

  const handleChange = (field, value) =>
    setForm((f) => ({ ...f, [field]: value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      annual_salary: Number(form.annual_salary) || 55000,
      automation_percentage: form.automation_percentage / 100,
      implementation_cost: Number(form.implementation_cost) || 8000,
      ongoing_annual_cost: Number(form.ongoing_annual_cost) || 2400,
      jurisdiction: form.jurisdiction,
    };
    const res = await execute(payload);
    if (res) setResult(res);
  };

  const chartData = buildCumulativeSavings(result);
  const breakEven = breakEvenMonth(result);

  // Normalise ROI fields — API may return 0–1 fraction or already-percent integer
  const normaliseRoi = (val) => {
    if (val == null) return null;
    const n = Number(val);
    // Heuristic: if >5, assume already expressed as percent
    return Math.abs(n) > 5 ? n : n * 100;
  };

  const year1Roi = normaliseRoi(result?.year_1_roi ?? result?.year1_roi_percent ?? null);
  const year3Roi = normaliseRoi(result?.year_3_roi ?? result?.year3_roi_percent ?? null);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Left – Form */}
      <Card className="bg-white shadow-sm rounded-xl border">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-lg">
            <Calculator className="h-5 w-5 text-violet-600" />
            Calculate Your ROI
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Estimate your automation return before committing a single dollar.
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Annual Salary */}
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1.5">
                Annual Salary (USD)
              </label>
              <Input
                type="number"
                min={0}
                placeholder="55000"
                value={form.annual_salary}
                onChange={(e) => handleChange('annual_salary', e.target.value)}
              />
            </div>

            {/* Automation Coverage – styled range */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-sm font-medium text-gray-700">
                  Automation Coverage
                </label>
                <span className="text-sm font-bold text-violet-600">
                  {form.automation_percentage}%
                </span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                step={5}
                value={form.automation_percentage}
                onChange={(e) => handleChange('automation_percentage', Number(e.target.value))}
                className="w-full h-2 rounded-full appearance-none cursor-pointer accent-violet-600 bg-gray-200"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>
            </div>

            {/* Implementation Cost */}
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1.5">
                Implementation Cost (USD)
              </label>
              <Input
                type="number"
                min={0}
                placeholder="8000"
                value={form.implementation_cost}
                onChange={(e) => handleChange('implementation_cost', e.target.value)}
              />
            </div>

            {/* Ongoing Annual Cost */}
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1.5">
                Ongoing Annual Cost (USD)
              </label>
              <Input
                type="number"
                min={0}
                placeholder="2400"
                value={form.ongoing_annual_cost}
                onChange={(e) => handleChange('ongoing_annual_cost', e.target.value)}
              />
            </div>

            {/* Jurisdiction */}
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1.5">
                Jurisdiction
              </label>
              <Select
                value={form.jurisdiction}
                onValueChange={(val) => handleChange('jurisdiction', val)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USA-Federal">USA — Federal</SelectItem>
                  <SelectItem value="Canada">Canada</SelectItem>
                  <SelectItem value="EU">EU</SelectItem>
                  <SelectItem value="Quebec-Law25">Quebec — Law 25</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {error && (
              <div className="flex items-center gap-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
                <AlertCircle className="h-4 w-4 shrink-0" />
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-violet-600 hover:bg-violet-700 text-white"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Calculating…
                </>
              ) : (
                <>
                  <Calculator className="h-4 w-4 mr-2" />
                  Calculate ROI
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Right – Results */}
      {result ? (
        <Card className="bg-white shadow-sm rounded-xl border">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 text-lg">
              <TrendingUp className="h-5 w-5 text-violet-600" />
              Your ROI Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            {/* 3 KPI tiles */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-violet-50 rounded-xl p-4 text-center border border-violet-100">
                <p className="text-[11px] text-violet-600 font-semibold uppercase tracking-wide leading-tight">
                  Payback Period
                </p>
                <p className="text-2xl font-bold text-violet-700 mt-1 tabular-nums">
                  {result.payback_months != null
                    ? `${Number(result.payback_months).toFixed(0)}mo`
                    : '—'}
                </p>
              </div>
              <div className="bg-emerald-50 rounded-xl p-4 text-center border border-emerald-100">
                <p className="text-[11px] text-emerald-600 font-semibold uppercase tracking-wide leading-tight">
                  Year 1 ROI
                </p>
                <p className="text-2xl font-bold text-emerald-700 mt-1 tabular-nums">
                  {year1Roi != null ? `${Math.round(year1Roi)}%` : '—'}
                </p>
              </div>
              <div className="bg-blue-50 rounded-xl p-4 text-center border border-blue-100">
                <p className="text-[11px] text-blue-600 font-semibold uppercase tracking-wide leading-tight">
                  Year 3 ROI
                </p>
                <p className="text-2xl font-bold text-blue-700 mt-1 tabular-nums">
                  {year3Roi != null ? `${Math.round(year3Roi)}%` : '—'}
                </p>
              </div>
            </div>

            {/* Annual savings row */}
            <div className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-4 py-3 border">
              <span className="text-gray-600 font-medium">Annual Savings</span>
              <span className="font-bold text-gray-900">{fmt$(result.annual_savings)}</span>
            </div>

            {/* Recommendation */}
            {result.recommendation && (
              <div className="flex gap-2 bg-violet-50 rounded-lg p-3 border border-violet-100">
                <CheckCircle className="h-4 w-4 text-violet-600 shrink-0 mt-0.5" />
                <p className="text-sm text-violet-800">{result.recommendation}</p>
              </div>
            )}

            {/* Cumulative savings chart */}
            <div>
              <p className="text-sm font-semibold text-gray-700 mb-2">
                Cumulative Savings — 36 Months
              </p>
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={chartData} margin={{ top: 8, right: 12, left: 4, bottom: 16 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis
                    dataKey="month"
                    ticks={[0, 6, 12, 18, 24, 30, 36]}
                    tick={{ fontSize: 10 }}
                    label={{ value: 'Month', position: 'insideBottom', offset: -4, fontSize: 11 }}
                  />
                  <YAxis
                    tick={{ fontSize: 10 }}
                    tickFormatter={(v) => fmt$(v)}
                    width={62}
                  />
                  <Tooltip content={<SavingsTooltip />} />
                  {breakEven != null && breakEven <= 36 && (
                    <ReferenceLine
                      x={breakEven}
                      stroke="#10b981"
                      strokeDasharray="4 3"
                      label={{ value: `Break-even ~${breakEven}mo`, position: 'top', fontSize: 10, fill: '#10b981' }}
                    />
                  )}
                  <ReferenceLine y={0} stroke="#e5e7eb" />
                  <Line
                    type="monotone"
                    dataKey="savings"
                    stroke="#7c3aed"
                    strokeWidth={2.5}
                    dot={{ r: 4, fill: '#7c3aed', strokeWidth: 0 }}
                    activeDot={{ r: 6 }}
                    name="Cumulative Savings"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="bg-gray-50 shadow-sm rounded-xl border flex items-center justify-center min-h-[420px]">
          <div className="text-center px-8 space-y-3">
            <div className="h-14 w-14 rounded-full bg-violet-100 flex items-center justify-center mx-auto">
              <TrendingUp className="h-7 w-7 text-violet-400" />
            </div>
            <p className="text-gray-500 text-sm">
              Fill in the form and click{' '}
              <span className="font-semibold text-violet-600">Calculate ROI</span>{' '}
              to see your personalized analysis.
            </p>
            <p className="text-xs text-gray-400">
              Results include payback period, ROI projections, and a savings timeline.
            </p>
          </div>
        </Card>
      )}
    </div>
  );
}

// ─── Section 2 – ROI Benchmarks ───────────────────────────────────────────────

function BenchmarksSection() {
  const { data, loading, error, refetch } = useApi(getROIBenchmarks, []);

  if (loading) return <LoadingCards count={5} className="grid-cols-2 sm:grid-cols-3 lg:grid-cols-5" />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  const rows = Array.isArray(data) ? data : [];

  if (!rows.length) {
    return (
      <p className="text-sm text-gray-400 py-8 text-center">No benchmark data available.</p>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {rows.map((bench, i) => {
        const months = bench.payback_months ?? bench.avg_payback_months;
        const accent = paybackCardAccent(months);
        return (
          <Card
            key={i}
            className={`bg-white shadow-sm rounded-xl border hover:shadow-md transition-shadow ${accent.border}`}
          >
            <CardContent className="p-5 space-y-3">
              <div className="flex items-center justify-between">
                <Building2 className="h-4 w-4 text-gray-300 shrink-0" />
              </div>
              <p className="text-sm font-semibold text-gray-800 leading-snug">
                {bench.company_size ?? `Tier ${i + 1}`}
              </p>
              <div className="space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-gray-500">Payback</span>
                  <span
                    className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-semibold border ${accent.badge}`}
                  >
                    {months != null ? `${months}mo` : '—'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-500">Success Rate</span>
                  <span className="font-medium text-gray-700">
                    {bench.success_rate != null
                      ? fmtPct(bench.success_rate, Math.abs(Number(bench.success_rate)) <= 1 ? 100 : 1)
                      : '—'}
                  </span>
                </div>
                {bench.typical_budget != null && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500">Budget</span>
                    <span className="font-medium text-gray-700">{fmt$(bench.typical_budget)}</span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

// ─── Section 3 – Task ROI Database ───────────────────────────────────────────

function TaskROIDatabase() {
  const { data, loading, error, refetch } = useApi(getRoiAnalysis, ['', '']);

  if (loading) return <LoadingTable rows={8} cols={6} />;
  if (error) return <ErrorState error={error} onRetry={refetch} />;

  const rows = Array.isArray(data) ? data : [];

  if (!rows.length) {
    return (
      <p className="text-sm text-gray-400 py-8 text-center">No ROI analysis data available.</p>
    );
  }

  // Sort by year1_roi_percent descending
  const sorted = [...rows].sort((a, b) => {
    const aVal = a.year1_roi_percent ?? a.year_1_roi ?? 0;
    const bVal = b.year1_roi_percent ?? b.year_1_roi ?? 0;
    return bVal - aVal;
  });

  // Normalise ROI value to percent integer
  const toPercent = (val) => {
    if (val == null) return null;
    const n = Number(val);
    return Math.abs(n) > 5 ? n : n * 100;
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-gray-50/80">
            {[
              'Task Description',
              'Occupation',
              'Annual Savings',
              'Payback',
              'Year 1 ROI',
              'Year 3 ROI',
            ].map((h) => (
              <th
                key={h}
                className="text-left px-3 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap"
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, i) => {
            const paybackMonths = row.payback_months ?? row.payback;
            const y1 = toPercent(row.year1_roi_percent ?? row.year_1_roi);
            const y3 = toPercent(row.year3_roi_percent ?? row.year_3_roi);
            const isTop3 = i < 3;
            return (
              <tr
                key={i}
                className={`border-b transition-colors hover:bg-gray-50 ${isTop3 ? 'bg-amber-50/40' : ''}`}
              >
                {/* Task Description */}
                <td className="px-3 py-3 max-w-[220px]">
                  <div className="flex items-center gap-2">
                    {isTop3 && (
                      <Star className="h-3.5 w-3.5 text-amber-500 shrink-0 fill-amber-400" />
                    )}
                    <span
                      className="font-medium text-gray-900 truncate block"
                      title={row.task_description ?? row.task_name ?? row.task ?? ''}
                    >
                      {row.task_description ?? row.task_name ?? row.task ?? '—'}
                    </span>
                  </div>
                </td>

                {/* Occupation */}
                <td className="px-3 py-3 text-gray-600 max-w-[140px]">
                  <span className="truncate block" title={row.occupation ?? ''}>
                    {row.occupation ?? '—'}
                  </span>
                </td>

                {/* Annual Savings */}
                <td className="px-3 py-3 font-semibold text-emerald-700 whitespace-nowrap tabular-nums">
                  {fmt$(row.annual_savings)}
                </td>

                {/* Payback */}
                <td className="px-3 py-3 whitespace-nowrap">
                  {paybackMonths != null ? (
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${paybackClass(paybackMonths)}`}
                    >
                      {paybackMonths}mo
                    </span>
                  ) : (
                    <span className="text-gray-400">—</span>
                  )}
                </td>

                {/* Year 1 ROI */}
                <td className="px-3 py-3 font-semibold text-violet-700 whitespace-nowrap tabular-nums">
                  {y1 != null ? `${Math.round(y1)}%` : '—'}
                </td>

                {/* Year 3 ROI */}
                <td className="px-3 py-3 font-semibold text-blue-700 whitespace-nowrap tabular-nums">
                  {y3 != null ? `${Math.round(y3)}%` : '—'}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ─── Page Root ────────────────────────────────────────────────────────────────

export default function ROICalculator() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <DollarSign className="h-6 w-6 text-violet-600" />
            ROI Calculator
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Model your automation ROI before committing a single dollar.
          </p>
        </div>

        {/* Section 1 – Interactive Calculator */}
        <CalculatorSection />

        {/* Section 2 – ROI Benchmarks */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Building2 className="h-5 w-5 text-violet-600" />
            <h2 className="text-lg font-semibold text-gray-900">ROI by Company Size</h2>
            <Badge variant="outline" className="text-xs ml-1">
              Color = payback speed
            </Badge>
          </div>
          <BenchmarksSection />
        </div>

        {/* Section 3 – Task ROI Database */}
        <Card className="bg-white shadow-sm rounded-xl border">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Clock className="h-5 w-5 text-violet-600" />
              Task ROI Analysis Database
            </CardTitle>
            <p className="text-sm text-gray-500 mt-0.5">
              Sorted by Year 1 ROI — highest first.{' '}
              <span className="inline-flex items-center gap-1 text-amber-600">
                <Star className="h-3.5 w-3.5 fill-amber-400" />
                = Best ROI (top 3)
              </span>
            </p>
          </CardHeader>
          <CardContent className="p-0 pt-2">
            <TaskROIDatabase />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
