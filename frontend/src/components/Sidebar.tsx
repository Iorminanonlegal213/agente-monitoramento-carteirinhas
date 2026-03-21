'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { clsx } from 'clsx';
import {
  LayoutDashboard, AlertTriangle, Users, Building2,
  Upload, Shield, Menu, X
} from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/alertas', label: 'Alertas', icon: AlertTriangle },
  { href: '/funcionarios', label: 'Funcionários', icon: Users },
  { href: '/consolidacao', label: 'Consolidação', icon: Building2 },
  { href: '/importacao', label: 'Importação', icon: Upload },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setOpen(!open)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-brand-500 text-white p-2 rounded-lg shadow-lg"
      >
        {open ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Overlay */}
      {open && (
        <div className="lg:hidden fixed inset-0 bg-black/40 z-30" onClick={() => setOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={clsx(
        'fixed lg:static inset-y-0 left-0 z-40 w-64 bg-[#0F2027] text-white flex flex-col transition-transform lg:translate-x-0',
        open ? 'translate-x-0' : '-translate-x-full'
      )}>
        <div className="p-5 border-b border-white/10">
          <div className="flex items-center gap-3">
            <Shield className="text-brand-400 shrink-0" size={28} />
            <div>
              <h1 className="text-sm font-bold leading-tight">Monitoramento</h1>
              <p className="text-xs text-brand-300">Carteirinhas & Requisitos</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {navItems.map(({ href, label, icon: Icon }) => {
            const active = pathname === href;
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setOpen(false)}
                className={clsx(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors',
                  active
                    ? 'bg-brand-500/20 text-brand-300 font-semibold'
                    : 'text-gray-400 hover:bg-white/5 hover:text-white'
                )}
              >
                <Icon size={18} />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/10 text-xs text-gray-500">
          GTIC • TBG • v1.0
        </div>
      </aside>
    </>
  );
}
