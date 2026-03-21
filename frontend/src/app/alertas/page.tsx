'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/AppShell';
import CriticidadeBadge from '@/components/CriticidadeBadge';
import { api } from '@/lib/api';
import { RefreshCw, Filter, ChevronDown, ChevronUp } from 'lucide-react';

export default function AlertasPage() {
  const [alertas, setAlertas] = useState<any>(null);
  const [empresas, setEmpresas] = useState<any[]>([]);
  const [unidades, setUnidades] = useState<string[]>([]);
  const [tipos, setTipos] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);

  // Filtros
  const [filtros, setFiltros] = useState({
    criticidade: '', faixa: '', empresa_id: '',
    unidade: '', tipo_item: '',
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = { limit: '100' };
      Object.entries(filtros).forEach(([k, v]) => { if (v) params[k] = v; });

      const [a, emp, uni, tp] = await Promise.all([
        api.getAlertas(params),
        api.getEmpresas(),
        api.getUnidades(),
        api.getTiposRequisito(),
      ]);
      setAlertas(a);
      setEmpresas(emp);
      setUnidades(uni);
      setTipos(tp);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => { loadData(); }, [filtros]);

  const resetFiltros = () => setFiltros({
    criticidade: '', faixa: '', empresa_id: '', unidade: '', tipo_item: '',
  });

  return (
    <AppShell>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Alertas Detalhados</h1>
          <p className="text-sm text-gray-500 mt-1">
            {alertas ? `${alertas.total} alertas encontrados` : 'Carregando…'}
          </p>
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
        >
          <Filter size={16} />
          Filtros
        </button>
      </div>

      {/* Filtros */}
      {showFilters && (
        <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Criticidade</label>
              <select value={filtros.criticidade} onChange={e => setFiltros(f => ({ ...f, criticidade: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="">Todas</option>
                <option value="critica">Crítica</option>
                <option value="alta">Alta</option>
                <option value="media">Média</option>
                <option value="baixa">Baixa</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Faixa</label>
              <select value={filtros.faixa} onChange={e => setFiltros(f => ({ ...f, faixa: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="">Todas</option>
                <option value="vencido">Vencido</option>
                <option value="vence_hoje">Vence hoje</option>
                <option value="ate_7_dias">Até 7 dias</option>
                <option value="ate_15_dias">Até 15 dias</option>
                <option value="ate_30_dias">Até 30 dias</option>
                <option value="ate_60_dias">Até 60 dias</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Empresa</label>
              <select value={filtros.empresa_id} onChange={e => setFiltros(f => ({ ...f, empresa_id: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="">Todas</option>
                {empresas.map((e: any) => <option key={e.id} value={e.id}>{e.razao_social}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Unidade</label>
              <select value={filtros.unidade} onChange={e => setFiltros(f => ({ ...f, unidade: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="">Todas</option>
                {unidades.map(u => <option key={u} value={u}>{u}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Tipo Requisito</label>
              <select value={filtros.tipo_item} onChange={e => setFiltros(f => ({ ...f, tipo_item: e.target.value }))}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="">Todos</option>
                {tipos.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
          </div>
          <button onClick={resetFiltros} className="mt-3 text-xs text-brand-500 hover:underline">
            Limpar filtros
          </button>
        </div>
      )}

      {/* Tabela */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        {loading ? (
          <div className="flex justify-center py-16">
            <RefreshCw className="animate-spin text-brand-500" size={24} />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                <tr>
                  <th className="px-4 py-3 text-left w-8"></th>
                  <th className="px-4 py-3 text-left">Funcionário</th>
                  <th className="px-4 py-3 text-left">Empresa</th>
                  <th className="px-4 py-3 text-left">Contrato</th>
                  <th className="px-4 py-3 text-left">Unidade</th>
                  <th className="px-4 py-3 text-left">Item</th>
                  <th className="px-4 py-3 text-center">Vencimento</th>
                  <th className="px-4 py-3 text-center">Dias</th>
                  <th className="px-4 py-3 text-center">Criticidade</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {alertas?.alertas?.map((a: any) => (
                  <>
                    <tr key={a.id} className="hover:bg-gray-50 cursor-pointer"
                      onClick={() => setExpanded(expanded === a.id ? null : a.id)}>
                      <td className="px-4 py-3">
                        {expanded === a.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900">{a.funcionario_nome}</td>
                      <td className="px-4 py-3 text-gray-600 max-w-[150px] truncate">{a.empresa_nome}</td>
                      <td className="px-4 py-3 text-gray-600 font-mono text-xs">{a.contrato_numero}</td>
                      <td className="px-4 py-3 text-gray-600">{a.unidade}</td>
                      <td className="px-4 py-3 text-gray-600 max-w-[200px] truncate">{a.item_descricao}</td>
                      <td className="px-4 py-3 text-center text-gray-600">
                        {a.data_vencimento || '—'}
                      </td>
                      <td className="px-4 py-3 text-center font-mono font-semibold">
                        <span className={a.dias_restantes !== null && a.dias_restantes < 0 ? 'text-red-600' : ''}>
                          {a.dias_restantes !== null ? a.dias_restantes : '—'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <CriticidadeBadge criticidade={a.criticidade} />
                      </td>
                    </tr>
                    {expanded === a.id && (
                      <tr key={`${a.id}-detail`} className="bg-gray-50">
                        <td colSpan={9} className="px-8 py-4">
                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 text-sm">
                            <div>
                              <p className="text-xs text-gray-400 uppercase">Status do Contrato</p>
                              <p className="font-medium">{a.contrato_status}</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-400 uppercase">Tipo</p>
                              <p className="font-medium">{a.tipo_item}</p>
                            </div>
                            <div className="lg:col-span-2">
                              <p className="text-xs text-gray-400 uppercase">Ação Recomendada</p>
                              <p className="font-medium text-brand-700">{a.acao_recomendada}</p>
                            </div>
                            <div className="lg:col-span-2">
                              <p className="text-xs text-gray-400 uppercase">Responsável Sugerido</p>
                              <p className="font-medium">{a.responsavel_sugerido}</p>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </>
                ))}
                {(!alertas?.alertas || alertas.alertas.length === 0) && (
                  <tr>
                    <td colSpan={9} className="px-4 py-12 text-center text-gray-400">
                      Nenhum alerta encontrado com os filtros selecionados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </AppShell>
  );
}
