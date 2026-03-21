'use client';
import { useState } from 'react';
import AppShell from '@/components/AppShell';
import { api } from '@/lib/api';
import { Upload, RefreshCw, CheckCircle, Database, Play } from 'lucide-react';

export default function ImportacaoPage() {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [processamentos, setProcessamentos] = useState<any[]>([]);
  const [loadingHist, setLoadingHist] = useState(false);

  const handleProcessar = async () => {
    setProcessing(true);
    setResult(null);
    try {
      const r = await api.processar();
      setResult(r);
      loadHistorico();
    } catch (err) {
      console.error(err);
      setResult({ error: 'Erro ao processar. Verifique se o backend está rodando.' });
    }
    setProcessing(false);
  };

  const loadHistorico = async () => {
    setLoadingHist(true);
    try {
      const p = await api.getProcessamentos();
      setProcessamentos(p);
    } catch (err) { console.error(err); }
    setLoadingHist(false);
  };

  return (
    <AppShell>
      <h1 className="text-2xl font-bold text-gray-900 mb-1">Importação e Processamento</h1>
      <p className="text-sm text-gray-500 mb-6">Carregar dados e executar processamento de vencimentos</p>

      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        {/* Card de processamento */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-brand-100 rounded-lg">
              <Play size={20} className="text-brand-600" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900">Processar Vencimentos</h2>
              <p className="text-xs text-gray-500">Analisa todos os requisitos e gera alertas</p>
            </div>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            O processamento lê todos os funcionários com contrato vigente, verifica datas de vencimento
            de requisitos e carteirinhas, classifica por criticidade e gera os alertas.
          </p>
          <button
            onClick={handleProcessar}
            disabled={processing}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition disabled:opacity-50 font-medium"
          >
            <RefreshCw size={16} className={processing ? 'animate-spin' : ''} />
            {processing ? 'Processando…' : 'Executar Processamento'}
          </button>

          {result && !result.error && (
            <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-2 text-green-700 font-medium mb-2">
                <CheckCircle size={16} />
                {result.mensagem}
              </div>
              <div className="grid grid-cols-2 gap-2 text-sm text-green-800">
                <p>Total: <strong>{result.total_registros}</strong></p>
                <p>Críticos: <strong>{result.total_criticos}</strong></p>
                <p>Altos: <strong>{result.total_altos}</strong></p>
                <p>Médios: <strong>{result.total_medios}</strong></p>
                <p>Baixos: <strong>{result.total_baixos}</strong></p>
                <p>Inconsistências: <strong>{result.total_inconsistencias}</strong></p>
              </div>
            </div>
          )}

          {result?.error && (
            <div className="mt-4 p-4 bg-red-50 rounded-lg border border-red-200 text-red-700 text-sm">
              {result.error}
            </div>
          )}
        </div>

        {/* Card de informações */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-brand-100 rounded-lg">
              <Database size={20} className="text-brand-600" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900">Sobre os Dados</h2>
              <p className="text-xs text-gray-500">Como carregar dados no sistema</p>
            </div>
          </div>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-700 mb-1">1. Banco de dados</p>
              <p>Execute os scripts SQL (<code className="text-xs bg-gray-200 px-1 rounded">schema.sql</code> e{' '}
              <code className="text-xs bg-gray-200 px-1 rounded">seeds.sql</code>) no PostgreSQL.</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-700 mb-1">2. Seeds de exemplo</p>
              <p>Os seeds incluem 5 empresas, 6 contratos, 15 funcionários e diversos requisitos com datas variadas.</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-700 mb-1">3. Processamento</p>
              <p>Clique em &quot;Executar Processamento&quot; para analisar todos os vencimentos e gerar alertas.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Histórico */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-700">Histórico de Processamentos</h2>
          <button onClick={loadHistorico} className="text-xs text-brand-500 hover:underline">
            Atualizar
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
              <tr>
                <th className="px-4 py-3 text-left">ID</th>
                <th className="px-4 py-3 text-left">Data</th>
                <th className="px-4 py-3 text-center">Total</th>
                <th className="px-4 py-3 text-center">Críticos</th>
                <th className="px-4 py-3 text-center">Altos</th>
                <th className="px-4 py-3 text-center">Médios</th>
                <th className="px-4 py-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {processamentos.map((p: any) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-mono text-xs">#{p.id}</td>
                  <td className="px-4 py-3 text-gray-600">
                    {new Date(p.data_execucao).toLocaleString('pt-BR')}
                  </td>
                  <td className="px-4 py-3 text-center font-semibold">{p.total_registros}</td>
                  <td className="px-4 py-3 text-center text-red-600">{p.total_criticos}</td>
                  <td className="px-4 py-3 text-center text-orange-600">{p.total_altos}</td>
                  <td className="px-4 py-3 text-center text-yellow-600">{p.total_medios}</td>
                  <td className="px-4 py-3 text-center">
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      {p.status}
                    </span>
                  </td>
                </tr>
              ))}
              {processamentos.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400">
                    Nenhum processamento realizado ainda.
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
