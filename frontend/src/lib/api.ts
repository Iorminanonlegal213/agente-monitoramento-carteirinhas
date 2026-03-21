const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const res = await fetch(`${API_URL}/api${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  // Resumo
  getResumo: () => fetchAPI('/resumo'),

  // Alertas
  getAlertas: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return fetchAPI(`/alertas${qs}`);
  },
  getAlertasCriticos: () => fetchAPI('/alertas/criticos'),

  // Consolidação
  getConsolidacaoEmpresas: () => fetchAPI('/consolidacao/empresas'),
  getConsolidacaoUnidades: () => fetchAPI('/consolidacao/unidades'),
  getConsolidacaoContratos: () => fetchAPI('/consolidacao/contratos'),

  // Dados
  getEmpresas: () => fetchAPI('/empresas'),
  getContratos: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return fetchAPI(`/contratos${qs}`);
  },
  getFuncionarios: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return fetchAPI(`/funcionarios${qs}`);
  },
  getRequisitosFuncionario: (id: number) => fetchAPI(`/funcionarios/${id}/requisitos`),
  getRequisitos: () => fetchAPI('/requisitos'),

  // Filtros
  getUnidades: () => fetchAPI('/filtros/unidades'),
  getTiposRequisito: () => fetchAPI('/filtros/tipos-requisito'),

  // Processamento
  processar: () => fetchAPI('/processar', { method: 'POST' }),
  getProcessamentos: () => fetchAPI('/processamentos'),
};
