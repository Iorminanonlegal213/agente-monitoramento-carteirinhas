'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/AppShell';
import StatCard from '@/components/StatCard';
import CriticidadeBadge from '@/components/CriticidadeBadge';
import { api } from '@/lib/api';
import {
  AlertTriangle, AlertCircle, Clock, CheckCircle,
  ShieldAlert, Users, Building2, RefreshCw
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

const PIE_COLORS = ['#dc2626', '#ea580c', '#eab308', '#22c55e', '#0891b2'];

export default function DashboardPage() {
  const [resumo, setResumo] = useState<any>(null);
  const [alertas, setAlertas] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [r, a] = await Promise.all([
        api.getResumo(),
        api.getAlertas({ limit: '10', resolvido: 'false' }),
      ]);
      setResumo(r);
      setAlertas(a);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
    }
    setLoading(false);
  };

  const handleProcessar = async () => {
    setProcessing(true);
    try {
      await api.processar();
      await loadData();
    } catch (err) {
      console.error('Erro ao processar:', err);
    }
    setProcessing(false);
  };

  useEffect(() => { loadData(); }, []);

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center h-96">
          <RefreshCw className="animate-spin text-brand-500" size={32} />
        </div>
      </AppShell>
    );
  }

  const pieData = resumo ? [
    { name: 'Crítico', value: resumo.total_criticos },
    { name: 'Alto', value: resumo.total_altos },
    { name: 'Médio', value: resumo.total_medios },
    { name: 'Baixo', value: resumo.total_baixos },
    { name: 'OK', value: resumo.total_ok },
  ].filter(d => d.value > 0) : [];

  const barData = resumo?.alertas_por_empresa?.map((e: any) => ({
    name: e.empresa.length > 15 ? e.empresa.substring(0, 15) + '…' : e.empresa,
    total: e.total,
    criticos: e.criticos,
  })) || [];

  return (
    <AppShell>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">
            Monitoramento Preventivo de Carteirinhas e Requisitos
          </p>
        </div>
        <button
          onClick={handleProcessar}
          disabled={processing}
          className="flex items-center gap-2 px-4 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition disabled:opacity-50 text-sm font-medium"
        >
          <RefreshCw size={16} className={processing ? 'animate-spin' : ''} />
          {processing ? 'Processando…' : 'Reprocessar'}
        </button>
      </div>

      {/* Stat Cards */}
      {resumo && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard title="Total de Alertas" value={resumo.total_alertas} icon={AlertTriangle} color="gray" />
          <StatCard title="Críticos" value={resumo.total_criticos} icon={ShieldAlert} color="red" subtitle="Ação imediata" />
          <StatCard title="Altos" value={resumo.total_altos} icon={AlertCircle} color="orange" subtitle="Até 7 dias" />
          <StatCard title="Médios" value={resumo.total_medios} icon={Clock} color="yellow" subtitle="Até 30 dias" />
        </div>
      )}

      {resumo && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard title="Baixos" value={resumo.total_baixos} icon={CheckCircle} color="green" subtitle="Até 60 dias" />
          <StatCard title="Funcionários Afetados" value={resumo.total_funcionarios_afetados} icon={Users} color="teal" />
          <StatCard title="Empresas Afetadas" value={resumo.total_empresas_afetadas} icon={Building2} color="teal" />
          <StatCard title="Inconsistências" value={resumo.total_inconsistencias} icon={AlertTriangle} color="yellow" subtitle="Cadastro" />
        </div>
      )}

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        {/* Pie */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Distribuição por Criticidade</h2>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-400 text-center py-16">Sem dados</p>
          )}
        </div>

        {/* Bar */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Alertas por Empresa</h2>
          {barData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={barData}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="total" fill="#0891b2" radius={[4, 4, 0, 0]} name="Total" />
                <Bar dataKey="criticos" fill="#dc2626" radius={[4, 4, 0, 0]} name="Críticos" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-400 text-center py-16">Sem dados</p>
          )}
        </div>
      </div>

      {/* Alertas recentes */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-5 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-700">Alertas Mais Urgentes</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
              <tr>
                <th className="px-4 py-3 text-left">Funcionário</th>
                <th className="px-4 py-3 text-left">Empresa</th>
                <th className="px-4 py-3 text-left">Unidade</th>
                <th className="px-4 py-3 text-left">Item</th>
                <th className="px-4 py-3 text-center">Dias</th>
                <th className="px-4 py-3 text-center">Criticidade</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {alertas?.alertas?.map((a: any) => (
                <tr key={a.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-900">{a.funcionario_nome}</td>
                  <td className="px-4 py-3 text-gray-600">{a.empresa_nome?.substring(0, 20)}</td>
                  <td className="px-4 py-3 text-gray-600">{a.unidade}</td>
                  <td className="px-4 py-3 text-gray-600">{a.item_descricao?.substring(0, 30)}</td>
                  <td className="px-4 py-3 text-center font-mono">
                    {a.dias_restantes !== null ? a.dias_restantes : '—'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <CriticidadeBadge criticidade={a.criticidade} />
                  </td>
                </tr>
              ))}
              {(!alertas?.alertas || alertas.alertas.length === 0) && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                    Nenhum alerta encontrado. Clique em &quot;Reprocessar&quot; para gerar alertas.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
