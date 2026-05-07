import { useEffect, useState } from "react";
import {
  TERMINAL_COMPLETION_SOUND_OPTIONS,
  type TerminalCompletionSoundId,
} from "../app/notificationSounds";
import { ActionButton } from "./ui/ActionButton";
import { SettingsToggle } from "./ui/SettingsToggle";

type SettingsPrimaryViewProps = {
  terminalCompletionSound: TerminalCompletionSoundId;
  isRuntimeStatusStripVisible: boolean;
  isMonitorVisible: boolean;
  onTerminalCompletionSoundChange: (soundId: TerminalCompletionSoundId) => void;
  onPreviewTerminalCompletionSound: (soundId: TerminalCompletionSoundId) => void;
  onRuntimeStatusStripVisibilityChange: (visible: boolean) => void;
  onMonitorVisibilityChange: (visible: boolean) => void;
};

type LLMConfig = {
  active_provider: string;
  providers: Record<string, { model: string }>;
};

export const SettingsPrimaryView = ({
  terminalCompletionSound,
  isRuntimeStatusStripVisible,
  isMonitorVisible,
  onTerminalCompletionSoundChange,
  onPreviewTerminalCompletionSound,
  onRuntimeStatusStripVisibilityChange,
  onMonitorVisibilityChange,
}: SettingsPrimaryViewProps) => {
  const [llmConfig, setLlmConfig] = useState<LLMConfig | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  // Carrega configuração via Claude/Terminal (simulado via prompt invisível ou fetch se disponível)
  useEffect(() => {
    fetch("/api/terminals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: "get-config",
        initialPrompt: "universal-brain.get_current_llm_config()",
        workspaceMode: "shared",
        isHidden: true
      })
    });
    // Como não temos um endpoint de leitura direta de arquivos sem MCP, 
    // a melhor forma no Octogent é via Ferramenta no Chat.
  }, []);

  return (
    <section className="settings-view" aria-label="Settings primary view">
      {/* NOVO PAINEL: Configuração de LLM */}
      <section className="settings-panel" aria-label="LLM Configuration">
        <header className="settings-panel-header">
          <h2>Universal Brain (Multi-LLM)</h2>
          <p>Configure qual IA será usada para tarefas de escrita e criatividade para economizar créditos do Claude.</p>
        </header>

        <div className="settings-llm-grid" style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
          <div className="settings-field">
            <label style={{ display: 'block', marginBottom: '0.5rem', opacity: 0.8 }}>Provedor Ativo</label>
            <select 
              style={{ background: '#222', color: '#fff', border: '1px solid #444', padding: '0.5rem', width: '100%' }}
              onChange={(e) => {
                const provider = e.target.value;
                // Envia comando para o terminal invisível
                window.dispatchEvent(new CustomEvent('octogent-cmd', { detail: `universal-brain.set_active_llm("${provider}")` }));
              }}
            >
              <option value="openrouter">OpenRouter (Grok, Gemini, etc)</option>
              <option value="groq">Groq (Llama 3.3)</option>
              <option value="openai">OpenAI (GPT-4o)</option>
            </select>
          </div>

          <div className="settings-field">
            <label style={{ display: 'block', marginBottom: '0.5rem', opacity: 0.8 }}>Modelo do OpenRouter</label>
            <input 
              type="text" 
              placeholder="ex: x-ai/grok-beta"
              style={{ background: '#222', color: '#fff', border: '1px solid #444', padding: '0.5rem', width: '100%' }}
              onBlur={(e) => {
                const model = e.target.value;
                if(model) window.dispatchEvent(new CustomEvent('octogent-cmd', { detail: `universal-brain.set_active_llm("openrouter", "${model}")` }));
              }}
            />
          </div>
        </div>

        <div className="settings-panel-actions">
           <span className="settings-saved-pill">Configurações aplicadas instantaneamente</span>
        </div>
      </section>

      <section className="settings-panel" aria-label="Completion notification settings">
        <header className="settings-panel-header">
          <h2>Tentacle completion sound</h2>
          <p>Play a notification when a tentacle moves from processing to idle.</p>
        </header>

        <div className="settings-sound-picker">
          {TERMINAL_COMPLETION_SOUND_OPTIONS.map((option) => (
            <button
              aria-pressed={terminalCompletionSound === option.id}
              className="settings-sound-option"
              data-active={terminalCompletionSound === option.id ? "true" : "false"}
              key={option.id}
              onClick={() => {
                onTerminalCompletionSoundChange(option.id);
                onPreviewTerminalCompletionSound(option.id);
              }}
              type="button"
            >
              <span className="settings-sound-option-label">{option.label}</span>
              <span className="settings-sound-option-description">{option.description}</span>
            </button>
          ))}
        </div>

        <div className="settings-panel-actions">
          <ActionButton
            aria-label="Preview selected completion sound"
            className="settings-sound-preview"
            onClick={() => {
              onPreviewTerminalCompletionSound(terminalCompletionSound);
            }}
            size="dense"
            variant="accent"
          >
            Preview
          </ActionButton>
          <span className="settings-saved-pill">Saved to workspace</span>
        </div>
      </section>
      
      <section className="settings-panel" aria-label="Workspace surface visibility settings">
        <header className="settings-panel-header">
          <h2>Workspace surface visibility</h2>
          <p>Enable or disable monitor surfaces in the main workspace shell.</p>
        </header>

        <div className="settings-toggle-grid">
          <SettingsToggle
            label="X Monitor"
            description="Auto-fetch X feed and show monitor tab"
            ariaLabel="Enable X Monitor"
            checked={isMonitorVisible}
            onChange={onMonitorVisibilityChange}
          />
          <SettingsToggle
            label="Runtime status strip"
            description="Top console status strip metrics"
            ariaLabel="Show runtime status strip"
            checked={isRuntimeStatusStripVisible}
            onChange={onRuntimeStatusStripVisibilityChange}
          />
        </div>
      </section>
    </section>
  );
};
