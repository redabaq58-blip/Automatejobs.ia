import { cn } from '@/lib/utils';

const tierConfig = {
  'Full': { bg: 'bg-emerald-100 text-emerald-800 border-emerald-200', dot: 'bg-emerald-500' },
  'High': { bg: 'bg-blue-100 text-blue-800 border-blue-200', dot: 'bg-blue-500' },
  'Medium': { bg: 'bg-amber-100 text-amber-800 border-amber-200', dot: 'bg-amber-500' },
  'Low': { bg: 'bg-orange-100 text-orange-800 border-orange-200', dot: 'bg-orange-500' },
  'None': { bg: 'bg-red-100 text-red-800 border-red-200', dot: 'bg-red-500' },
};

export function getScoreColor(score) {
  if (score >= 86) return 'text-emerald-600';
  if (score >= 61) return 'text-blue-600';
  if (score >= 31) return 'text-amber-600';
  return 'text-red-600';
}

export function getScoreBg(score) {
  if (score >= 86) return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  if (score >= 61) return 'bg-blue-50 text-blue-700 border-blue-200';
  if (score >= 31) return 'bg-amber-50 text-amber-700 border-amber-200';
  return 'bg-red-50 text-red-700 border-red-200';
}

export function ScoreBadge({ score, tier, className }) {
  const config = tierConfig[tier] || tierConfig['None'];
  const displayScore = typeof score === 'number' ? Math.round(score) : null;

  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border',
      config.bg,
      className
    )}>
      <span className={cn('h-1.5 w-1.5 rounded-full', config.dot)} />
      {displayScore !== null ? `${displayScore}/100` : tier}
    </span>
  );
}

export function TierBadge({ tier, className }) {
  const config = tierConfig[tier] || tierConfig['None'];
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium border',
      config.bg,
      className
    )}>
      {tier || 'None'}
    </span>
  );
}

export function ScoreBar({ score, className }) {
  const color = score >= 86 ? 'bg-emerald-500' : score >= 61 ? 'bg-blue-500' : score >= 31 ? 'bg-amber-500' : 'bg-red-500';
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="flex-1 bg-gray-200 rounded-full h-1.5">
        <div
          className={cn('h-1.5 rounded-full transition-all', color)}
          style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
        />
      </div>
      <span className={cn('text-xs font-medium tabular-nums', getScoreColor(score))}>
        {Math.round(score)}
      </span>
    </div>
  );
}
