import type { TerminalCompletionSoundId } from "./completionSound";
import type { TerminalAgentProvider } from "./agentRuntime";

export type PersistedUiState = {
  activePrimaryNav?: number;
  isAgentsSidebarVisible?: boolean;
  sidebarWidth?: number;
  isActiveAgentsSectionExpanded?: boolean;
  isRuntimeStatusStripVisible?: boolean;
  isMonitorVisible?: boolean;
  isBottomTelemetryVisible?: boolean;
  isCodexUsageVisible?: boolean;
  isClaudeUsageVisible?: boolean;
  isClaudeUsageSectionExpanded?: boolean;
  isCodexUsageSectionExpanded?: boolean;
  terminalCompletionSound?: TerminalCompletionSoundId;
  preferredAgentProvider?: TerminalAgentProvider;
  minimizedTerminalIds?: string[];
  terminalWidths?: Record<string, number>;
  canvasOpenTerminalIds?: string[];
  canvasOpenTentacleIds?: string[];
  canvasTerminalsPanelWidth?: number;
  terminalInactivityThresholdMs?: number;
};
