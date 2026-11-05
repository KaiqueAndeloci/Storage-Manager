# Frontend — Storage Manager

Aplicação web do Storage Manager, desenvolvida com Next.js, React e TypeScript.

## Arquitetura

- `src/app/`: páginas, layouts e estilos da aplicação usando o App Router do Next.js.
- `src/components/`: componentes reutilizáveis da interface, incluindo componentes próprios e componentes de UI.
- `src/requests/API_backend/`: funções que fazem as chamadas para a API e tratam o fluxo de autenticação.
- `src/lib/` e `src/Providers/`: utilitários, sessão e provedores compartilhados.

O frontend se comunica com o backend em `http://127.0.0.1:8000`. Esse endereço está definido em `src/requests/API_backend/index.tsx`.

## Requisitos

- Node.js 20.9 ou superior.
- npm.
- Backend iniciado em `http://127.0.0.1:8000`.

## Instalação e execução

Na pasta `frontend/Development/storage-manager`, instale as dependências e inicie o servidor de desenvolvimento:

```bash
npm ci
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador. Para executar a aplicação, inicie também o backend conforme as instruções em [`backend/README.md`](../../../backend/README.md).

## Outros comandos

```bash
npm run lint
npm run build
npm start
```

`npm start` executa a versão de produção; antes, gere-a com `npm run build`.
