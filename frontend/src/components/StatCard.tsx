import { clsx } from 'clsx';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: number | string;
  subtitle?: string;
  icon: LucideIcon;
  color?: 'red' | 'orange' | 'yellow' | 'green' | 'teal' | 'gray';
}

const colorMap = {
  red: 'bg-red-50 text-red-600 border-red-200',
  orange: 'bg-orange-50 text-orange-600 border-orange-200',
  yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200',
  green: 'bg-green-50 text-green-600 border-green-200',
  teal: 'bg-brand-50 text-brand-600 border-brand-200',
  gray: 'bg-gray-50 text-gray-600 border-gray-200',
};

const iconBg = {
  red: 'bg-red-100 text-red-500',
  orange: 'bg-orange-100 text-orange-500',
  yellow: 'bg-yellow-100 text-yellow-500',
  green: 'bg-green-100 text-green-500',
  teal: 'bg-brand-100 text-brand-500',
  gray: 'bg-gray-100 text-gray-500',
};

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'teal' }: StatCardProps) {
  return (
    <div className={clsx('rounded-xl border p-4 lg:p-5', colorMap[color])}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide opacity-70">{title}</p>
          <p className="text-2xl lg:text-3xl font-bold mt-1">{value}</p>
          {subtitle && <p className="text-xs mt-1 opacity-60">{subtitle}</p>}
        </div>
        <div className={clsx('p-2 rounded-lg', iconBg[color])}>
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}
