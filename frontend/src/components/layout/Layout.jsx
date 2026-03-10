import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';

const pageTitles = {
  '/': 'Executive Dashboard',
  '/occupations': 'Occupation Explorer',
  '/skills': 'Skills Intelligence',
  '/regulatory': 'Regulatory Compliance',
  '/industries': 'Industry Intelligence',
  '/roi': 'ROI Calculator',
  '/vendors': 'Vendor Intelligence',
  '/arbitrage': 'Labor Arbitrage',
  '/build': 'Build Studio',
  '/build/wizard': 'AI Wizard',
  '/build/blueprints': 'My Blueprints',
  '/build/chat': 'AI Assistant',
};

export function Layout() {
  const location = useLocation();
  const title = pageTitles[location.pathname] || 'Automatejobs.ia';

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden ml-64">
        {/* Top Header */}
        <header className="h-14 border-b bg-card flex items-center justify-between px-6 shrink-0">
          <div>
            <h1 className="text-sm font-semibold text-foreground">{title}</h1>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="/build/wizard"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-violet-600 text-white text-xs font-medium rounded-lg hover:bg-violet-700 transition-colors"
            >
              + New Automation
            </a>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
