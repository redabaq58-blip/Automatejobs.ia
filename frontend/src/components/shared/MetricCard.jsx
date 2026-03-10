import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export function MetricCard({ title, value, subtitle, icon: Icon, trend, color = 'violet', className }) {
  const colorMap = {
    violet: 'text-violet-600 bg-violet-50',
    blue: 'text-blue-600 bg-blue-50',
    emerald: 'text-emerald-600 bg-emerald-50',
    amber: 'text-amber-600 bg-amber-50',
    red: 'text-red-600 bg-red-50',
  };
  const iconColor = colorMap[color] || colorMap.violet;

  return (
    <Card className={cn('border shadow-sm hover:shadow-md transition-shadow', className)}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold mt-1 text-foreground truncate">{value}</p>
            {subtitle && <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>}
            {trend && (
              <p className={cn('text-xs mt-1', trend.positive ? 'text-emerald-600' : 'text-red-600')}>
                {trend.positive ? '↑' : '↓'} {trend.label}
              </p>
            )}
          </div>
          {Icon && (
            <div className={cn('h-10 w-10 rounded-lg flex items-center justify-center shrink-0 ml-4', iconColor)}>
              <Icon className="h-5 w-5" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
