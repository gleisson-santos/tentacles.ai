import { cpSync, existsSync as fsExistsSync, mkdirSync, readdirSync } from "node:fs";
import { createServer } from "node:http";
import { join } from "node:path";

import { scanClaudeUsageChart } from "./claudeSessionScanner";
import {
  invalidateUsageCache as invalidateUsageCacheDefault,
  readClaudeCliUsageSnapshot as readClaudeCliUsageSnapshotDefault,
  readClaudeOauthUsageSnapshot as readClaudeOauthUsageSnapshotDefault,
  readClaudeUsageSnapshot as readClaudeUsageSnapshotDefault,
} from "./claudeUsage";
import { createCodeIntelStore } from "./codeIntelStore";
import { readCodexUsageSnapshot as readCodexUsageSnapshotDefault } from "./codexUsage";
import { createApiRequestHandler } from "./createApiServer/requestHandler";
import type { CreateApiServerOptions } from "./createApiServer/types";
import { createUpgradeHandler } from "./createApiServer/upgradeHandler";
import { readGithubRepoSummary as readGithubRepoSummaryDefault } from "./githubRepoSummary";
import { createMonitorService } from "./monitor";
import { LocalTrendsProvider } from "./monitor/localTrendsProvider";
import { createTerminalRuntime } from "./terminalRuntime";

export const createApiServer = ({
  workspaceCwd,
  projectStateDir,
  promptsDir,
  webDistDir,
  apiBaseUrl,
  gitClient,
  readClaudeUsageSnapshot,
  readClaudeOauthUsageSnapshot,
  readClaudeCliUsageSnapshot,
  readCodexUsageSnapshot = readCodexUsageSnapshotDefault,
  readGithubRepoSummary,
  scanUsageHeatmap,
  monitorService,
  invalidateClaudeUsageCache = invalidateUsageCacheDefault,
  allowRemoteAccess = false,
}: CreateApiServerOptions = {}) => {
  const resolvedWorkspaceCwd = workspaceCwd ?? process.cwd();
  const resolvedStateDir = projectStateDir ?? join(resolvedWorkspaceCwd, ".octogent");
  
  let resolvedApiBaseUrl = apiBaseUrl ?? "http://127.0.0.1:8787";
  const getApiBaseUrl = () => resolvedApiBaseUrl;
  const getApiPort = () => {
    try {
      return String(new URL(resolvedApiBaseUrl).port || 80);
    } catch {
      return "8787";
    }
  };

  const runtimeOptions: Parameters<typeof createTerminalRuntime>[0] = {
    workspaceCwd: resolvedWorkspaceCwd,
    projectStateDir: resolvedStateDir,
    getApiBaseUrl,
  };
  if (gitClient) {
    runtimeOptions.gitClient = gitClient;
  }

  const runtime = createTerminalRuntime(runtimeOptions);

  const resolvedMonitorService = monitorService ?? createMonitorService({
    projectStateDir: resolvedStateDir,
    providers: [new LocalTrendsProvider(resolvedWorkspaceCwd, () => runtime)]
  });

  const resolvedUserPromptsDir = join(resolvedStateDir, "prompts");
  const resolvedCorePromptsDir = join(resolvedStateDir, "prompts", "core");

  const sourceDir = promptsDir ?? join(resolvedWorkspaceCwd, "prompts");
  if (fsExistsSync(sourceDir)) {
    mkdirSync(resolvedCorePromptsDir, { recursive: true });
    for (const file of readdirSync(sourceDir)) {
      if (file.endsWith(".md")) {
        cpSync(join(sourceDir, file), join(resolvedCorePromptsDir, file));
      }
    }
  }

  const resolvedPromptsDir = fsExistsSync(sourceDir) ? sourceDir : resolvedCorePromptsDir;
  const readClaudeUsageSnapshotWithDefault =
    readClaudeUsageSnapshot ??
    (() =>
      readClaudeUsageSnapshotDefault({
        projectStateDir: resolvedStateDir,
        backgroundRefreshOnly: true,
      }));
  const readClaudeOauthUsageSnapshotWithDefault =
    readClaudeOauthUsageSnapshot ??
    (() =>
      readClaudeOauthUsageSnapshotDefault({
        projectStateDir: resolvedStateDir,
      }));
  const readClaudeCliUsageSnapshotWithDefault =
    readClaudeCliUsageSnapshot ??
    (() =>
      readClaudeCliUsageSnapshotDefault({
        projectStateDir: resolvedStateDir,
      }));
  const readGithubRepoSummaryWithDefault =
    readGithubRepoSummary ??
    (() =>
      readGithubRepoSummaryDefault({
        cwd: resolvedWorkspaceCwd,
      }));

  const scanUsageHeatmapWithDefault =
    scanUsageHeatmap ??
    ((scope: "all" | "project") => scanClaudeUsageChart(scope, resolvedWorkspaceCwd));

  const codeIntelStore = createCodeIntelStore(resolvedStateDir);

  const requestHandler = createApiRequestHandler({
    runtime,
    workspaceCwd: resolvedWorkspaceCwd,
    projectStateDir: resolvedStateDir,
    promptsDir: resolvedPromptsDir,
    userPromptsDir: resolvedUserPromptsDir,
    webDistDir,
    getApiBaseUrl,
    getApiPort,
    readClaudeUsageSnapshot: readClaudeUsageSnapshotWithDefault,
    readClaudeOauthUsageSnapshot: readClaudeOauthUsageSnapshotWithDefault,
    readClaudeCliUsageSnapshot: readClaudeCliUsageSnapshotWithDefault,
    readCodexUsageSnapshot,
    readGithubRepoSummary: readGithubRepoSummaryWithDefault,
    scanUsageHeatmap: scanUsageHeatmapWithDefault,
    monitorService: resolvedMonitorService,
    invalidateClaudeUsageCache,
    codeIntelStore,
    allowRemoteAccess,
  });

  const server = createServer(requestHandler);

  server.on(
    "upgrade",
    createUpgradeHandler({
      runtime,
      allowRemoteAccess,
    }),
  );

  return {
    server,
    async start(port = 8787, host = "127.0.0.1") {
      await new Promise<void>((resolveStart, rejectStart) => {
        server.listen(port, host, () => resolveStart());
        server.once("error", rejectStart);
      });

      const address = server.address();
      const resolvedPort = typeof address === "object" && address ? address.port : port;
      resolvedApiBaseUrl = `http://${host}:${resolvedPort}`;

      return { host, port: resolvedPort };
    },
    async stop() {
      await runtime.close();
      await new Promise<void>((resolveStop, rejectStop) => {
        server.close((error) => {
          if (error) {
            rejectStop(error);
            return;
          }
          resolveStop();
        });
        server.closeAllConnections();
      });
    },
  };
};
