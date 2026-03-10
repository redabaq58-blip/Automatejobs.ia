import { useNavigate } from 'react-router-dom';
import { ArrowRight, TrendingUp, Bot } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ScoreBar } from '@/components/shared/ScoreBadge';
import { LoadingCards, ErrorState } from '@/components/shared/LoadingState';
import { useApi } from '@/hooks/useApi';
import { getAllIndustries, getTaskQuickWins } from '@/lib/api';

const FEATURED_PLAYBOOKS = [
  {
    title: 'Invoice Processing Automation',
    industry: 'Finance',
    payback: 3.2,
    description: 'Automate invoice capture, validation, and approval workflows end-to-end.',
  },
  {
    title: 'HR Onboarding AI Agent',
    industry: 'Human Resources',
    payback: 5.1,
    description: 'Guide new hires through paperwork, training, and system access automatically.',
  },
  {
    title: 'Customer Support Triage',
    industry: 'Customer Service',
    payback: 4.7,
    description: 'Classify, route, and resolve tier-1 support tickets with AI.',
  },
];

function getMaturityStyle(score) {
  if (score > 70) return 'bg-emerald-50 border-emerald-200';
  if (score >= 50) return 'bg-blue-50 border-blue-200';
  return 'bg-amber-50 border-amber-200';
}

function getMaturityLabel(score) {
  if (score > 70) return { label: 'High Readiness', color: 'text-emerald-700' };
  if (score >= 50) return { label: 'Growing', color: 'text-blue-700' };
  return { label: 'Early Stage', color: 'text-amber-700' };
}

function getEffortColor(effort) {
  const e = (effort || '').toLowerCase();
  if (e.includes('low') || e.includes('easy')) return 'bg-emerald-100 text-emerald-800';
  if (e.includes('medium')) return 'bg-blue-100 text-blue-800';
  return 'bg-amber-100 text-amber-800';
}

export default function BuildHome() {
  const navigate = useNavigate();

  const { data: industries, loading: industriesLoading, error: industriesError, refetch: refetchIndustries } =
    useApi(getAllIndustries, [], []);

  const { data: quickWins, loading: quickWinsLoading, error: quickWinsError, refetch: refetchQuickWins } =
    useApi(getTaskQuickWins, [8], []);

  const industryList = Array.isArray(industries) ? industries : (industries?.industries || []);
  const quickWinList = Array.isArray(quickWins) ? quickWins : (quickWins?.tasks || quickWins?.quick_wins || []);

  return (
    <div className="space-y-16 pb-16">
      {/* Hero */}
      <section className="py-12 text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-50 border border-violet-200 text-violet-700 text-sm font-medium">
          <Bot className="h-4 w-4" />
          Builder Studio — No coding required
        </div>
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 max-w-3xl mx-auto leading-tight">
          Build Enterprise AI Automations
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          No experience needed. Pick an industry, and AI guides you to a complete automation blueprint —
          compliant in USA, Canada &amp; Europe.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto mt-8 text-left">
          <Card
            className="border-2 border-emerald-300 cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => navigate('/build/wizard?mode=quick')}
          >
            <CardContent className="p-6 space-y-2">
              <div className="text-2xl">⚡</div>
              <h3 className="font-semibold text-gray-900">Quick Wins</h3>
              <p className="text-sm text-muted-foreground">
                Find the easiest tasks to automate in 5 minutes
              </p>
              <Button variant="ghost" size="sm" className="text-emerald-600 px-0 hover:text-emerald-700">
                Get started <ArrowRight className="ml-1 h-3 w-3" />
              </Button>
            </CardContent>
          </Card>

          <Card
            className="border-2 border-blue-300 cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => {
              document.getElementById('industry-explorer')?.scrollIntoView({ behavior: 'smooth' });
            }}
          >
            <CardContent className="p-6 space-y-2">
              <div className="text-2xl">🏭</div>
              <h3 className="font-semibold text-gray-900">Browse by Industry</h3>
              <p className="text-sm text-muted-foreground">
                Explore automations for your specific sector
              </p>
              <Button variant="ghost" size="sm" className="text-blue-600 px-0 hover:text-blue-700">
                Browse industries <ArrowRight className="ml-1 h-3 w-3" />
              </Button>
            </CardContent>
          </Card>

          <Card
            className="border-2 border-violet-300 cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => navigate('/build/wizard')}
          >
            <CardContent className="p-6 space-y-2">
              <div className="text-2xl">🤖</div>
              <h3 className="font-semibold text-gray-900">AI Guided Wizard</h3>
              <p className="text-sm text-muted-foreground">
                Step-by-step guidance to a full blueprint
              </p>
              <Button variant="ghost" size="sm" className="text-violet-600 px-0 hover:text-violet-700">
                Start wizard <ArrowRight className="ml-1 h-3 w-3" />
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Quick Wins */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Quick Win Automations</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Low-effort, high-impact tasks you can start automating this week
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={() => navigate('/build/wizard?mode=quick')}>
            See all quick wins
          </Button>
        </div>

        {quickWinsLoading && <LoadingCards count={6} />}
        {quickWinsError && <ErrorState error={quickWinsError} onRetry={refetchQuickWins} />}

        {!quickWinsLoading && !quickWinsError && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {quickWinList.slice(0, 6).map((task, i) => (
              <Card key={task.id || i} className="hover:shadow-sm transition-shadow">
                <CardContent className="p-5 space-y-3">
                  <p className="text-sm font-medium text-gray-800 line-clamp-2">
                    {task.task || task.task_description || task.title || 'Automation Task'}
                  </p>
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>
                      Payback:{' '}
                      <span className="font-semibold text-emerald-700">
                        {task.payback_months
                          ? `${task.payback_months} months`
                          : task.implementation_weeks
                          ? `~${Math.ceil(task.implementation_weeks / 4)} months`
                          : '< 6 months'}
                      </span>
                    </span>
                    {(task.effort || task.difficulty) && (
                      <span
                        className={`px-2 py-0.5 rounded-full font-medium ${getEffortColor(
                          task.effort || task.difficulty
                        )}`}
                      >
                        {task.effort || task.difficulty}
                      </span>
                    )}
                  </div>
                  {task.automation_score != null && (
                    <ScoreBar score={task.automation_score} />
                  )}
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full text-violet-600 border-violet-200 hover:bg-violet-50"
                    onClick={() => navigate('/build/wizard', { state: { quickWinTask: task } })}
                  >
                    Start Building →
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>

      {/* Industry Explorer */}
      <section id="industry-explorer" className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Explore by Industry</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Click an industry to start building automations tailored to your sector
          </p>
        </div>

        {industriesLoading && <LoadingCards count={8} />}
        {industriesError && <ErrorState error={industriesError} onRetry={refetchIndustries} />}

        {!industriesLoading && !industriesError && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
            {industryList.map((ind, i) => {
              const score =
                ind.maturity_score ?? ind.automation_maturity ?? ind.avg_automation_score ?? 50;
              const maturity = getMaturityLabel(score);
              const cardStyle = getMaturityStyle(score);
              const taskCount = ind.task_count ?? ind.automation_tasks ?? ind.total_tasks ?? null;

              return (
                <Card
                  key={ind.industry || ind.name || i}
                  className={`cursor-pointer border hover:shadow-md transition-all ${cardStyle}`}
                  onClick={() =>
                    navigate('/build/wizard', {
                      state: { preselectedIndustry: ind.industry || ind.name },
                    })
                  }
                >
                  <CardContent className="p-4 space-y-2">
                    <h3 className="font-semibold text-sm text-gray-900 leading-tight">
                      {ind.industry || ind.name}
                    </h3>
                    <ScoreBar score={score} />
                    <div className="flex items-center justify-between">
                      <span className={`text-xs font-medium ${maturity.color}`}>
                        {maturity.label}
                      </span>
                      {taskCount != null && (
                        <span className="text-xs text-muted-foreground">{taskCount} tasks</span>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </section>

      {/* Featured Playbooks */}
      <section className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Popular Automation Playbooks</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Proven blueprints used by forward-thinking teams
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {FEATURED_PLAYBOOKS.map((pb) => (
            <Card key={pb.title} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-base leading-snug">{pb.title}</CardTitle>
                  <Badge variant="outline" className="text-xs shrink-0">
                    {pb.industry}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground">{pb.description}</p>
                <div className="flex items-center gap-2 text-sm">
                  <TrendingUp className="h-4 w-4 text-emerald-500" />
                  <span className="text-emerald-700 font-semibold">
                    Payback: {pb.payback} months
                  </span>
                </div>
                <Button
                  className="w-full bg-violet-600 hover:bg-violet-700 text-white"
                  size="sm"
                  onClick={() => navigate('/build/wizard')}
                >
                  View Blueprint
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
