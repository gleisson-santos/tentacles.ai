# 🐙 Tentacles.ai — Plataforma de Agentes de Produtividade

**Tentacles.ai** (anteriormente Clilink) é um ecossistema multi-agente robusto projetado para automatizar fluxos de trabalho complexos, gestão de mídias sociais e tarefas de produtividade através de uma interface unificada orquestrada pelo **Octogent** e **Claude Code**.

## 🚀 Visão Geral

O sistema utiliza o protocolo **MCP (Model Context Protocol)** para conectar modelos de linguagem de grande escala (LLMs) a ferramentas do mundo real, permitindo automações que vão desde postagens inteligentes no LinkedIn até a criação de apresentações executivas e gestão de e-mails.

## ✨ Funcionalidades Principais

### 📱 Automação de Mídias Sociais (LinkedIn)
- **Auto-Poster:** Geração e publicação automática de conteúdo relevante a cada 2 horas.
- **Inteligência:** Analisa tendências via Google News usando Groq (LLaMA 3.3).
- **Visual:** Geração de imagens minimalistas e profissionais via Stability AI.

### 📧 Gestão de Produtividade (Google Workspace)
- **Gmail:** Leitura, busca e envio de e-mails automatizados.
- **Calendar:** Gestão de agenda, criação de eventos e verificação de disponibilidade.
- **Sheets:** Manipulação de planilhas para extração e inserção de dados.

### 📄 Geração de Documentos (Files)
- **PDFs:** Criação de documentos estruturados (contratos, relatórios, dietas).
- **PowerPoint:** Geração automática de apresentações profissionais.

### 🧠 Cérebro Universal (Multi-LLM)
- **Flexibilidade:** Troca dinâmica de modelos (Grok, GPT-4o, Llama 3.3, Gemini) via Dashboard ou Telegram.
- **Economia:** Usa Claude Code para orquestração e LLMs externas (OpenRouter/Groq) para geração de conteúdo longo.
- **Gestão de Chaves:** Configuração segura de chaves de API diretamente pelo chat.

### 🤖 Interface de Comando (Telegram & Dashboard)
- **Telegram Bot:** Controle total do sistema via chat, com detecção de intenção inteligente.
- **Octogent Dashboard:** Interface visual para monitoramento e orquestração dos "tentáculos" (agentes).

## 🏗️ Arquitetura

O projeto é estruturado em torno de "Tentáculos", onde cada um possui uma responsabilidade específica e comunica-se através do barramento de eventos do Octogent.

- **Orquestrador:** Claude Code atuando como o cérebro central.
- **MCP Servers:** Servidores dedicados para Google APIs e File Systems.
- **Bridge:** Sistema de comunicação entre o bot do Telegram e o Dashboard Octogent.

## 🛠️ Tecnologias

- **IA:** Groq (LLaMA 3.3), Stability AI.
- **Linguagens:** Python 3.14+, Node.js 22+.
- **Protocolos:** FastMCP, OAuth2, WebSockets.
- **Dashboard:** Octogent (Customizado).

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.14+
- Node.js 22+ (para o Octogent)
- Pnpm (gerenciador de pacotes Node)

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/tentacles.ai.git
   cd tentacles.ai
   ```
2. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale as dependências do Octogent:
   ```bash
   cd octogent
   pnpm install
   cd ..
   ```

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
GROQ_API_KEY=sua_chave_aqui
STABILITY_KEY=sua_chave_aqui
TELEGRAM_BOT_TOKEN=seu_token_aqui
ALLOWED_USER_ID=seu_id_telegram
```

## 🚀 Como Usar

1. **Inicie o Dashboard:**
   ```bash
   octogent
   ```
2. **Inicie o Bot do Telegram:**
   ```bash
   python bots/telegram_bot.py
   ```
3. **Inicie o Auto-Poster (Opcional):**
   ```bash
   python auto_poster.py
   ```

## 📂 Estrutura do Projeto

- `octogent/`: Código fonte do Dashboard e interface web.
- `mcp_servers/`: Servidores MCP para integração com APIs externas.
- `bots/`: Implementação do bot de interface (Telegram).
- `scripts/`: Utilitários para criação e sincronização de agentes.
- `logs/`: Logs de atividade e eventos.
- `outputs/`: Repositório de arquivos gerados (PDFs, PPTXs).
- `.claude/`: Skills e regras de comportamento dos agentes.

---
*Desenvolvido com ❤️ para máxima produtividade.*
