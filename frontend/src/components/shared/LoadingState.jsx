import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

export function LoadingCards({ count = 4, className }) {
  return (
    <div className={cn('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4', className)}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="rounded-xl border bg-card p-6 space-y-3">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-3 w-20" />
        </div>
      ))}
    </div>
  );
}

export function LoadingTable({ rows = 5, cols = 4, className }) {
  return (
    <div className={cn('space-y-2', className)}>
      <div className="flex gap-4 pb-2 border-b">
        {Array.from({ length: cols }).map((_, i) => (
          <Skeleton key={i} className="h-4 flex-1" />
        ))}
      </div>
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 py-2">
          {Array.from({ length: cols }).map((_, j) => (
            <Skeleton key={j} className="h-4 flex-1" />
          ))}
        </div>
      ))}
    </div>
  );
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="h-12 w-12 rounded-full bg-red-50 flex items-center justify-center mb-3">
        <span className="text-red-500 text-xl">⚠</span>
      </div>
      <p className="text-sm font-medium text-foreground">Failed to load data</p>
      <p className="text-xs text-muted-foreground mt-1">{error}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 text-xs text-violet-600 hover:text-violet-700 font-medium"
        >
          Try again
        </button>
      )}
    </div>
  );
}
