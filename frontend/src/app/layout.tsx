import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Monitoramento de Carteirinhas',
  description: 'Agente de Monitoramento Preventivo de Carteirinhas e Requisitos de Acesso',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
