import { readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import type {
  MonitorPost,
  MonitorProviderAdapter,
  MonitorProviderId,
} from "./types";

export class LocalTrendsProvider implements MonitorProviderAdapter {
  public providerId: MonitorProviderId = "x";
  private workspaceCwd: string;
  private getTerminalRuntime?: () => any;

  constructor(workspaceCwd: string, getTerminalRuntime?: () => any) {
    this.workspaceCwd = workspaceCwd;
    this.getTerminalRuntime = getTerminalRuntime;
  }

  async fetchRecentPosts(args: { queryTerms: string[] }): Promise<MonitorPost[]> {
    const configPath = join(this.workspaceCwd, "config", "monitor_config.json");
    const filePath = join(this.workspaceCwd, "outputs", "trends_data.json");

    try {
      // 1. Sincroniza termos
      const config = {
        searchTerms: args.queryTerms,
        refreshIntervalMinutes: 30
      };
      await writeFile(configPath, JSON.stringify(config, null, 2));

      // 2. Dispara o Agente se o runtime estiver disponível
      if (this.getTerminalRuntime) {
        const runtime = this.getTerminalRuntime();
        const uiState = runtime.readUiState();
        const preferredProvider = uiState.preferredAgentProvider || "claude-code";
        
        const tentacleId = "trends-intelligence";
        const allTerminals = runtime.listTerminalSnapshots();
        
        // Limpeza: Deleta terminais "stale" ou "exited" deste tentáculo para evitar poluição
        const prunable = allTerminals.filter(t => t.tentacleId === tentacleId && (t.state === "stale" || t.state === "exited"));
        for (const t of prunable) {
          try { runtime.deleteTerminal(t.terminalId); } catch {}
        }

        const existingLive = allTerminals.find((t: any) => t.tentacleId === tentacleId && t.state === "live");

        const prompt = `ATUALIZAÇÃO DE TENDÊNCIAS REQUISITADA:
1. Leia os termos em config/monitor_config.json.
2. Execute o script 'python scripts/trends_monitor.py --loop' para manter o monitoramento ativo e contínuo.
3. O Dashboard lerá os resultados automaticamente de 'outputs/trends_data.json'.
4. Mantenha este terminal aberto para monitoramento em tempo real.`;

        if (existingLive) {
          // Só envia se não estiver ocupado (idle) ou se passou muito tempo
          if (existingLive.agentRuntimeState === "idle") {
             runtime.writeInput(existingLive.terminalId, `${prompt}\n`);
          }
        } else {
          // Cria novo terminal com o prompt inicial
          runtime.createTerminal({
            tentacleId,
            tentacleName: "Trends Intelligence Agent",
            workspaceMode: "shared",
            agentProvider: preferredProvider,
            initialPrompt: prompt
          });
        }
      }

      // 3. Lê o resultado atual
      let data: any = { google_news: [] };
      try {
        const content = await readFile(filePath, "utf-8");
        data = JSON.parse(content);
      } catch {
        // Arquivo pode não existir na primeira rodada
      }
      
      const posts: MonitorPost[] = [];
      if (data.google_news) {
        for (const item of data.google_news) {
          const summaryText = item.summary || "Resumo sendo gerado pelo agente...";
          const analysisTime = item.analysis_time || "Aguardando agente...";
          
          posts.push({
            source: "google-news",
            id: item.link,
            text: `📢 ${item.title}\n\n🤖 ANÁLISE IA (${analysisTime}):\n${summaryText}\n\n🔗 Ver matéria original no Google News`,
            // Título mais limpo conforme solicitado
            author: `Trends Intelligence`,
            createdAt: analysisTime.includes("/") ? new Date().toISOString() : item.published,
            likeCount: 0,
            permalink: item.link,
            matchedQueryTerm: "News"
          });
        }
      }

      return posts;
    } catch (e) {
      console.error("LocalTrendsProvider error:", e);
      return [];
    }
  }

  async fetchUsage() {
    return {
      cap: 100,
      used: 0,
      remaining: 100,
      window7d: 0,
      resets: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };
  }

  summarizeCredentials() {
    return { status: "Trends Intelligence Agent Active" };
  }

  saveCredentials(input: any) {
    return { credentials: { token: "local" } };
  }

  async validateCredentials(): Promise<{ ok: boolean }> {
    return { ok: true };
  }
}

export const createLocalTrendsProvider = (workspaceCwd: string, getTerminalRuntime?: () => any) => 
  new LocalTrendsProvider(workspaceCwd, getTerminalRuntime);
