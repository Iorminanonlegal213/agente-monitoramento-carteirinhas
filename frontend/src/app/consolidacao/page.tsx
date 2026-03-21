'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/AppShell';
import { api } from '@/lib/api';
import { RefreshCw, Building2, MapPin, FileText } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { clsx } from 'clsx';

type Tab = 'empresas' | 'unidades' | 'contratos';

export default function ConsolidacaoPage() {
  const [tab, setTab] = useState<Tab>('empresas');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      let result;
      if (tab === 'empresas') result = await api.getConsolidacaoEmpresas();
      else if (tab === 'unidades') result = await api.getConsolidacaoUnidades();
      else result = await api.getConsolidacaoContratos();
      setData(result);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  useEffect(() => { loadData(); }, [tab]);

  const tabs = [
    { key: 'empresas' as Tab, label: 'Por Empresa', icon: Building2 },
    { key: 'unidades' as Tab, label: 'Por Unidade', icon: MapPin },
    { key: 'contratos' as Tab, label: 'Por Contrato', icon: FileText },
  ];

  const chartData = data.map(d => ({
    name: (d.empresa_nome || d.unidade || d.contrato_numero || '').substring(0, 18),
    Críticos: d.criticos,
    Altos: d.altos,
    Médios: d.medios,
    Baixos: d.baixos,
  }));

  return (
    <AppShell>
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Consolidação</h1>
      <p className="text-sm text-gray-500 mb-6">Visão agregada dos alertas por dimensão</p>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {tabs.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={clsx(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition',
              tab === key
                ? 'bg-brand-500 text-white'
                : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'
            )}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <RefreshCw className="animate-spin text-brand-500" size={24} />
        </div>
      ) : (
        <>
          {/* Chart */}
          {chartData.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-4">
                Distribuição de Alertas {tab === 'empresas' ? 'por Empresa' : tab === 'unidades' ? 'por Unidade' : 'por Contrato'}
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="Críticos" stackId="a" fill="#dc2626" />
                  <Bar dataKey="Altos" stackId="a" fill="#ea580c" />
                  <Bar dataKey="Médios" stackId="a" fill="#eab308" />
                  <Bar dataKey="Baixos" stackId="a" fill="#22c55e" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Table */}
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                  <tr>
                    <th className="px-4 py-3 text-left">
                      {tab === 'empresas' ? 'Empresa' : tab === 'unidades' ? 'Unidade' : 'Contrato'}
                    </th>
                    {tab === 'contratos' && <th className="px-4 py-3 text-left">Empresa</th>}
                    {tab === 'contratos' && <th className="px-4 py-3 text-left">Unidade</th>}
                    <th className="px-4 py-3 text-center">Total</th>
                    <th className="px-4 py-3 text-center">Críticos</th>
                    <th className="px-4 py-3 text-center">Altos</th>
                    <th className="px-4 py-3 text-center">Médios</th>
                    <th className="px-4 py-3 text-center">Baixos</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {data.map((d: any, i: number) => (
                    <tr key={i} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900">
                        {d.empresa_nome || d.unidade || d.contrato_numero}
                      </td>
                      {tab === 'contratos' && <td className="px-4 py-3 text-gray-600">{d.empresa_nome}</td>}
                      {tab === 'contratos' && <td className="px-4 py-3 text-gray-600">{d.unidade}</td>}
                      <td className="px-4 py-3 text-center font-semibold">{d.total_alertas}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={d.criticos > 0 ? 'text-red-600 font-bold' : 'text-gray-400'}>{d.criticos}</span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={d.altos > 0 ? 'text-orange-600 font-semibold' : 'text-gray-400'}>{d.altos}</span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={d.medios > 0 ? 'text-yellow-600' : 'text-gray-400'}>{d.medios}</span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="text-gray-500">{d.baixos}</span>
                      </td>
                    </tr>
                  ))}
                  {data.length === 0 && (
                    <tr>
                      <td colSpan={7} className="px-4 py-12 text-center text-gray-400">
                        Nenhum dado encontrado. Execute o processamento primeiro.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </AppShell>
  );
}
