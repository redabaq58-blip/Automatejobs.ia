import { cn } from '@/lib/utils';

const jurisdictionConfig = {
  'USA-Federal': { label: '🇺🇸 USA', bg: 'bg-blue-50 text-blue-700 border-blue-200' },
  'Canada': { label: '🇨🇦 Canada', bg: 'bg-red-50 text-red-700 border-red-200' },
  'EU': { label: '🇪🇺 EU', bg: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
  'Quebec-Law25': { label: '🇨🇦 Quebec', bg: 'bg-orange-50 text-orange-700 border-orange-200' },
};

const impactConfig = {
  'BLOCKS': { bg: 'bg-red-100 text-red-800 border-red-200' },
  'RESTRICTS': { bg: 'bg-amber-100 text-amber-800 border-amber-200' },
  'ENABLES': { bg: 'bg-emerald-100 text-emerald-800 border-emerald-200' },
  'MONITORS': { bg: 'bg-blue-100 text-blue-800 border-blue-200' },
};

export function JurisdictionBadge({ jurisdiction, className }) {
  const config = jurisdictionConfig[jurisdiction] || { label: jurisdiction, bg: 'bg-gray-100 text-gray-700 border-gray-200' };
  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border', config.bg, className)}>
      {config.label}
    </span>
  );
}

export function ImpactBadge({ impact, className }) {
  const config = impactConfig[impact] || { bg: 'bg-gray-100 text-gray-700 border-gray-200' };
  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border', config.bg, className)}>
      {impact}
    </span>
  );
}

export function ThreatBadge({ level, className }) {
  const config = {
    'CRITICAL': 'bg-red-100 text-red-800 border-red-200',
    'HIGH': 'bg-amber-100 text-amber-800 border-amber-200',
    'MEDIUM': 'bg-blue-100 text-blue-800 border-blue-200',
    'LOW': 'bg-emerald-100 text-emerald-800 border-emerald-200',
  }[level] || 'bg-gray-100 text-gray-700 border-gray-200';
  return (
    <span className={cn('inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border', config, className)}>
      {level}
    </span>
  );
}
