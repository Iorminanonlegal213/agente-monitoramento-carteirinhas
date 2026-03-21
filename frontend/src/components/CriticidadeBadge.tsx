import { clsx } from 'clsx';

const styles: Record<string, string> = {
  critica: 'bg-red-100 text-red-700 border-red-200',
  alta: 'bg-orange-100 text-orange-700 border-orange-200',
  media: 'bg-yellow-100 text-yellow-700 border-yellow-200',
  baixa: 'bg-green-100 text-green-700 border-green-200',
  ok: 'bg-teal-100 text-teal-700 border-teal-200',
};

const labels: Record<string, string> = {
  critica: 'Crítica',
  alta: 'Alta',
  media: 'Média',
  baixa: 'Baixa',
  ok: 'OK',
};

export default function CriticidadeBadge({ criticidade }: { criticidade: string }) {
  return (
    <span className={clsx(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border',
      styles[criticidade] || 'bg-gray-100 text-gray-700'
    )}>
      {labels[criticidade] || criticidade}
    </span>
  );
}
