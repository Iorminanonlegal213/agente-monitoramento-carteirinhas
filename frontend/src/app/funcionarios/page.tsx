'use client';
import { useEffect, useState } from 'react';
import AppShell from '@/components/AppShell';
import { api } from '@/lib/api';
import { RefreshCw, ChevronDown, ChevronUp, AlertTriangle, CheckCircle } from 'lucide-react';

export default function FuncionariosPage() {
  const [funcionarios, setFuncionarios] = useState<any[]>([]);
  const [empresas, setEmpresas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [requisitos, setRequisitos] = useState<any[]>([]);
  const [loadingReqs, setLoadingReqs] = useState(false);
  const [filtroEmpresa, setFiltroEmpresa] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (filtroEmpresa) params.empresa_id = filtroEmpresa;
      const [f, e] = await Promise.all([api.getFuncionarios(params), api.getEmpresas()]);
      setFuncionarios(f);
      setEmpresas(e);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const loadRequisitos = async (funcId: number) => {
    setLoadingReqs(true);
    try {
      const r = await api.getRequisitosFuncionario(funcId);
      setRequisitos(r);
    } catch (err) { console.error(err); }
    setLoadingReqs(false);
  };

  const handleExpand = (id: number) => {
    if (expanded === id) {
      setExpanded(null);
    } else {
      setExpanded(id);
      loadRequisitos(id);
    }
  };

  useEffect(() => { loadData(); }, [filtroEmpresa]);

  const diasColor = (dias: number | null) => {
    if (dias === null) return 'text-yellow-600';
    if (dias < 0) return 'text-red-600 font-bold';
    if (dias <= 7) return 'text-orange-600 font-bold';
    if (dias <= 30) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <AppShell>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Funcionários e Requisitos</h1>
          <p className="text-sm text-gray-500 mt-1">{funcionarios.length} funcionários encontrados</p>
        </div>
        <select value={filtroEmpresa} onChange={e => setFiltroEmpresa(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
          <option value="">Todas as empresas</option>
          {empresas.map((e: any) => <option key={e.id} value={e.id}>{e.razao_social}</option>)}
        </select>
      </div>

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
                  <th className="px-4 py-3 w-8"></th>
                  <th className="px-4 py-3 text-left">Nome</th>
                  <th className="px-4 py-3 text-left">Cargo</th>
                  <th className="px-4 py-3 text-left">Empresa</th>
                  <th className="px-4 py-3 text-left">Contrato</th>
                  <th className="px-4 py-3 text-left">Unidade</th>
                  <th className="px-4 py-3 text-center">Contrato Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {funcionarios.map((f: any) => (
                  <>
                    <tr key={f.id} className="hover:bg-gray-50 cursor-pointer" onClick={() => handleExpand(f.id)}>
                      <td className="px-4 py-3">
                        {expanded === f.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900">{f.nome}</td>
                      <td className="px-4 py-3 text-gray-600">{f.cargo}</td>
                      <td className="px-4 py-3 text-gray-600 max-w-[150px] truncate">{f.empresa_nome}</td>
                      <td className="px-4 py-3 text-gray-600 font-mono text-xs">{f.contrato_numero}</td>
                      <td className="px-4 py-3 text-gray-600">{f.contrato_unidade}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          f.contrato_status === 'vigente'
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-500'
                        }`}>
                          {f.contrato_status}
                        </span>
                      </td>
                    </tr>
                    {expanded === f.id && (
                      <tr key={`${f.id}-reqs`} className="bg-gray-50">
                        <td colSpan={7} className="px-8 py-4">
                          <h3 className="text-xs font-semibold text-gray-500 uppercase mb-3">Requisitos do Funcionário</h3>
                          {loadingReqs ? (
                            <RefreshCw className="animate-spin text-brand-500" size={16} />
                          ) : requisitos.length > 0 ? (
                            <div className="space-y-2">
                              {requisitos.map((r: any) => (
                                <div key={r.id} className="flex items-center justify-between bg-white rounded-lg border px-4 py-2">
                                  <div className="flex items-center gap-3">
                                    {r.inconsistencia ? (
                                      <AlertTriangle size={16} className="text-yellow-500" />
                                    ) : r.dias_restantes !== null && r.dias_restantes < 0 ? (
                                      <AlertTriangle size={16} className="text-red-500" />
                                    ) : (
                                      <CheckCircle size={16} className="text-green-500" />
                                    )}
                                    <div>
                                      <p className="font-medium text-sm">{r.requisito_nome}</p>
                                      <p className="text-xs text-gray-400">{r.categoria} • {r.numero_documento}</p>
                                    </div>
                                  </div>
                                  <div className="text-right">
                                    {r.inconsistencia ? (
                                      <p className="text-xs text-yellow-600 font-medium">Sem data de vencimento</p>
                                    ) : (
                                      <>
                                        <p className="text-xs text-gray-500">Venc: {r.data_vencimento}</p>
                                        <p className={`text-sm font-mono ${diasColor(r.dias_restantes)}`}>
                                          {r.dias_restantes} dias
                                        </p>
                                      </>
                                    )}
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <p className="text-gray-400 text-sm">Nenhum requisito cadastrado.</p>
                          )}
                        </td>
                      </tr>
                    )}
                  </>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </AppShell>
  );
}
