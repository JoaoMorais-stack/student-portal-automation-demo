# Student Portal Automation Demo

> English first. Versão em português abaixo.

## English

### Objective

This repository is a portfolio-safe reconstruction of a student portal automation concept. It demonstrates application architecture, local HTTP integration, progress tracking, a responsive interface, and defensive automation boundaries without connecting to any institution or third-party platform.

### Problem

Portal workflows often contain repetitive navigation and status updates. Reproducing those workflows against a real service would introduce authorization, privacy, reliability, and terms-of-use concerns. This project solves the portfolio problem with a fictional portal that runs entirely on the developer's machine and exposes only a purpose-built mock API.

### Features

- Fictional student, courses, instructors, lessons, and progress data.
- Responsive local portal with course status and an automation activity trace.
- One-click authorized demonstration from the browser.
- Command-line automation client for the same local mock.
- Resettable in-memory state; no personal data or database files.
- Explicit target validation that blocks non-loopback addresses, credentials in URLs, HTTPS targets, and URL paths.
- Local-only server binding enforced in code.
- Automated tests for HTTP behavior, progress updates, idempotency, and network boundaries.

### Technologies

- Python 3.10+ standard library
- `http.server` with a threaded local server
- HTML5, CSS3, and vanilla JavaScript
- `unittest` for automated verification
- `urllib` for the local automation client

No package download is required to run the source version.

### Architecture

```text
Browser UI
   | local HTTP
   v
Mock portal server ----> In-memory fictional data
   ^
   | local HTTP only
Automation client
```

The portal server binds to a loopback address. `PortalClient` validates its target before every workflow can begin and accepts only a plain-HTTP loopback origin. The automation reads fictional pending lessons from the mock API and records their completion through that same API.

### Installation

Prerequisite: Python 3.10 or newer.

Clone or download the repository, then enter its directory. The application has no runtime dependencies outside Python's standard library.

Optional editable installation:

```powershell
python -m pip install -e .
```

### Run

Start the mock portal:

```powershell
python run_demo.py
```

The browser opens at `http://127.0.0.1:8765`. Use **Run authorized demo** to process all pending fictional lessons. Use **Reset demo** to restore the initial state.

To keep the browser closed at startup:

```powershell
python run_demo.py serve --no-browser
```

With the server running, the standalone local automation can be demonstrated in a second terminal:

```powershell
python run_demo.py automate
```

### Demonstration

1. Start the local portal.
2. Review the fictional courses and initial progress.
3. Run the authorized demo from the interface or command line.
4. Observe each pending mock lesson become complete and appear in the local activity trace.
5. Reset the data and repeat the flow.

### Project structure

```text
student-portal-automation-demo/
|-- src/student_portal_demo/
|   |-- automation.py     # Local-only client and target validation
|   |-- models.py         # Fictional domain models and seed data
|   |-- server.py         # Mock HTTP portal and API
|   |-- store.py          # Thread-safe in-memory state
|   `-- static/           # Responsive browser interface
|-- tests/                # Safety, server, and workflow tests
|-- run_demo.py           # Source checkout entry point
|-- pyproject.toml        # Package metadata
|-- LICENSE
`-- README.md
```

### Limitations

- This is not an integration template for a real portal.
- State is intentionally reset when the server stops.
- The demo does not perform login, browser control, media playback, attendance, assessment, scraping, or third-party network access.
- The mock workflow is intentionally small and deterministic.

### Security and privacy

All names and academic records are fictional. The server rejects non-loopback binding, and the automation rejects non-loopback targets. No credentials, cookies, tokens, external URLs, real selectors, analytics, or telemetry are included. Use the project only as a local portfolio demonstration.

### Status

Functional portfolio demo. The core local workflow and automated safety checks are complete.

### Next steps

- Add an optional Playwright adapter that remains restricted to the bundled mock.
- Add accessibility regression checks.
- Package a signed desktop launcher for non-technical demonstrations.
- Add CI for supported Python versions.

## Português

### Objetivo

Este repositório é uma reconstrução segura para portfólio de um conceito de automação de portal estudantil. Ele demonstra arquitetura de aplicação, integração HTTP local, acompanhamento de progresso, interface responsiva e limites defensivos de automação sem se conectar a qualquer instituição ou plataforma de terceiros.

### Problema

Fluxos de portais costumam ter navegação e atualizações de estado repetitivas. Reproduzir esses fluxos em um serviço real traria questões de autorização, privacidade, confiabilidade e termos de uso. Este projeto resolve a necessidade de portfólio com um portal fictício executado inteiramente no computador do desenvolvedor e uma API mock criada especificamente para a demonstração.

### Funcionalidades

- Dados fictícios de estudante, disciplinas, docentes, aulas e progresso.
- Portal local responsivo com andamento dos cursos e histórico da automação.
- Demonstração autorizada com um clique no navegador.
- Cliente de automação por linha de comando para o mesmo mock local.
- Estado em memória que pode ser restaurado, sem dados pessoais ou arquivos de banco.
- Validação explícita que bloqueia endereços fora do loopback, credenciais em URLs, alvos HTTPS e caminhos adicionais.
- Servidor restrito a endereço local por código.
- Testes automatizados de HTTP, progresso, idempotência e limites de rede.

### Tecnologias

- Biblioteca padrão do Python 3.10+
- `http.server` com servidor local multithread
- HTML5, CSS3 e JavaScript puro
- `unittest` para verificação automatizada
- `urllib` para o cliente local de automação

Nenhum pacote precisa ser baixado para executar a versão-fonte.

### Arquitetura

```text
Interface no navegador
   | HTTP local
   v
Servidor mock ---------> Dados fictícios em memória
   ^
   | somente HTTP local
Cliente de automação
```

O servidor é vinculado a um endereço de loopback. O `PortalClient` valida o destino antes de iniciar qualquer fluxo e aceita somente uma origem loopback em HTTP. A automação consulta as aulas fictícias pendentes na API mock e registra a conclusão por essa mesma API.

### Instalação

Pré-requisito: Python 3.10 ou mais recente.

Clone ou baixe o repositório e entre na pasta. A aplicação não possui dependências de execução além da biblioteca padrão do Python.

Instalação editável opcional:

```powershell
python -m pip install -e .
```

### Execução

Inicie o portal mock:

```powershell
python run_demo.py
```

O navegador abrirá em `http://127.0.0.1:8765`. Use **Run authorized demo** para processar as aulas fictícias pendentes. Use **Reset demo** para restaurar o estado inicial.

Para iniciar sem abrir o navegador:

```powershell
python run_demo.py serve --no-browser
```

Com o servidor em execução, demonstre a automação local em um segundo terminal:

```powershell
python run_demo.py automate
```

### Demonstração

1. Inicie o portal local.
2. Confira as disciplinas fictícias e o progresso inicial.
3. Execute a demonstração autorizada pela interface ou linha de comando.
4. Observe cada aula mock pendente ser concluída e registrada no histórico local.
5. Restaure os dados para repetir o fluxo.

### Estrutura

```text
student-portal-automation-demo/
|-- src/student_portal_demo/
|   |-- automation.py     # Cliente local e validação do destino
|   |-- models.py         # Modelos e dados fictícios
|   |-- server.py         # Portal e API HTTP mock
|   |-- store.py          # Estado em memória protegido para threads
|   `-- static/           # Interface responsiva no navegador
|-- tests/                # Testes de segurança, servidor e fluxo
|-- run_demo.py           # Entrada para execução pelo código-fonte
|-- pyproject.toml        # Metadados do pacote
|-- LICENSE
`-- README.md
```

### Limitações

- Este projeto não é um modelo de integração com portais reais.
- O estado é restaurado quando o servidor encerra.
- A demonstração não faz login, controle de navegador, reprodução de mídia, presença, avaliações, scraping ou acesso de rede a terceiros.
- O fluxo mock é intencionalmente pequeno e determinístico.

### Segurança e privacidade

Todos os nomes e registros acadêmicos são fictícios. O servidor rejeita vinculação fora do loopback e a automação rejeita destinos fora do loopback. Não há credenciais, cookies, tokens, URLs externas, seletores reais, métricas ou telemetria. Use o projeto somente como demonstração local de portfólio.

### Status

Demonstração funcional para portfólio. O fluxo local principal e as verificações automatizadas de segurança estão concluídos.

### Próximos passos

- Adicionar um adaptador opcional de Playwright restrito ao mock incluído.
- Adicionar testes de regressão de acessibilidade.
- Empacotar um inicializador desktop assinado para demonstrações não técnicas.
- Adicionar integração contínua para versões suportadas do Python.

## License

See [LICENSE](LICENSE). All rights reserved.
