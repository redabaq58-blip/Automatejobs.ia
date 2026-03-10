import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Search, Brain, Shield, Factory,
  Calculator, Package, TrendingUp, Bot, Zap,
  Wand2, BookOpen, MessageSquare, ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';

const exploreNav = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/occupations', icon: Search, label: 'Occupations' },
  { to: '/skills', icon: Brain, label: 'Skills Intelligence' },
  { to: '/regulatory', icon: Shield, label: 'Regulatory' },
  { to: '/industries', icon: Factory, label: 'Industries' },
  { to: '/roi', icon: Calculator, label: 'ROI Calculator' },
  { to: '/vendors', icon: Package, label: 'Vendor Intelligence' },
  { to: '/arbitrage', icon: TrendingUp, label: 'Labor Arbitrage' },
];

const buildNav = [
  { to: '/build', icon: Zap, label: 'Start Building' },
  { to: '/build/wizard', icon: Wand2, label: 'AI Wizard' },
  { to: '/build/blueprints', icon: BookOpen, label: 'My Blueprints' },
  { to: '/build/chat', icon: MessageSquare, label: 'AI Assistant' },
];

function NavItem({ to, icon: Icon, label, exact }) {
  const location = useLocation();
  const isActive = exact ? location.pathname === to : location.pathname === to;

  return (
    <NavLink
      to={to}
      end={exact}
      className={({ isActive }) => cn(
        'sidebar-nav-item flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium',
        isActive
          ? 'bg-white/10 text-white'
          : 'text-slate-400 hover:text-white hover:bg-white/5'
      )}
    >
      <Icon className="h-4 w-4 shrink-0" />
      <span className="truncate">{label}</span>
    </NavLink>
  );
}

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-50 w-64 flex flex-col"
      style={{ background: 'hsl(224 71% 4%)' }}>
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-4 h-14 border-b border-white/10 shrink-0">
        <div className="h-7 w-7 rounded-lg bg-violet-600 flex items-center justify-center">
          <Bot className="h-4 w-4 text-white" />
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-white truncate">Automatejobs.ia</p>
          <p className="text-xs text-slate-500">Intelligence Platform</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-5">
        {/* Explore Section */}
        <div>
          <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Explore
          </p>
          <div className="space-y-0.5">
            {exploreNav.map(item => (
              <NavItem key={item.to} {...item} exact={item.to === '/'} />
            ))}
          </div>
        </div>

        {/* Build Section */}
        <div>
          <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Build
          </p>
          <div className="space-y-0.5">
            {buildNav.map(item => (
              <NavItem key={item.to} {...item} />
            ))}
          </div>
        </div>
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-white/10 shrink-0">
        <div className="flex items-center gap-2 px-3 py-2">
          <div className="h-2 w-2 rounded-full bg-emerald-400" />
          <span className="text-xs text-slate-500">v1.0.0 · 85+ endpoints</span>
        </div>
      </div>
    </aside>
  );
}
