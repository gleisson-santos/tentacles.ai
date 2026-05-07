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

export const SettingsPrimaryView = ({
  terminalCompletionSound,
  isRuntimeStatusStripVisible,
  isMonitorVisible,
  onTerminalCompletionSoundChange,
  onPreviewTerminalCompletionSound,
  onRuntimeStatusStripVisibilityChange,
  onMonitorVisibilityChange,
}: SettingsPrimaryViewProps) => {
  const [provider, setProvider] = useState("openrouter");
  const [model, setModel] = useState("openai/gpt-4o-mini-2024-07-18");
  const [apiKey, setApiKey] = useState("");
  const [isSaved, setIsSaved] = useState(false);

  const envMap: Record<string, string> = {
    openrouter: "OPENROUTER_API_KEY",
    groq: "GROQ_API_KEY",
    openai: "OPENAI_API_KEY",
    gemini: "GEMINI_API_KEY",
    claude: "CLAUDE_API_KEY"
  };

  const handleSave = () => {
    setIsSaved(false);
    window.dispatchEvent(new CustomEvent('octogent-cmd', { 
      detail: `universal-brain.set_active_llm("${provider}", "${model}")` 
    }));
    if (apiKey) {
      const envName = envMap[provider] || `${provider.toUpperCase()}_API_KEY`;
      window.dispatchEvent(new CustomEvent('octogent-cmd', { 
        detail: `universal-brain.update_env_key("${envName}", "${apiKey}")` 
      }));
    }
    setTimeout(() => setIsSaved(true), 500);
    setTimeout(() => setIsSaved(false), 3000);
  };

  return (
    <section className="settings-view" aria-label="Settings primary view">
      <section className="settings-panel" aria-label="LLM Configuration">
        <header className="settings-panel-header">
          <h2>Universal Brain (Multi-LLM)</h2>
          <p>Escolha qual IA orquestra as tarefas e economize créditos do Claude.</p>
        </header>
        <div className="settings-llm-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
          <div className="settings-field">
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#aaa' }}>Provedor</label>
            <select value={provider} style={{ background: '#1a1a1a', color: '#fff', border: '1px solid #333', padding: '0.6rem', width: '100%', borderRadius: '4px' }} onChange={(e) => setProvider(e.target.value)}>
              <option value="openrouter">OpenRouter (Grok, Gemini, Llama)</option>
              <option value="claude">Claude (Nativo)</option>
              <option value="groq">Groq</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>
          <div className="settings-field">
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#aaa' }}>Modelo</label>
            <input type="text" value={model} style={{ background: '#1a1a1a', color: '#fff', border: '1px solid #333', padding: '0.6rem', width: '100%', borderRadius: '4px' }} onChange={(e) => setModel(e.target.value)} />
          </div>
          <div className="settings-field" style={{ gridColumn: 'span 2' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#aaa' }}>Chave de API (Opcional)</label>
            <input type="password" placeholder="••••••••••••••••" style={{ background: '#1a1a1a', color: '#fff', border: '1px solid #333', padding: '0.6rem', width: '100%', borderRadius: '4px' }} onChange={(e) => setApiKey(e.target.value)} />
          </div>
        </div>
        <div className="settings-panel-actions" style={{ marginTop: '1.5rem' }}>
          <ActionButton onClick={handleSave} size="dense" variant="accent">Salvar Configurações de IA</ActionButton>
          {isSaved && <span className="settings-saved-pill" style={{ marginLeft: '1rem', color: '#4caf50' }}>✓ Configurações de IA salvas!</span>}
        </div>
      </section>

      <section className="settings-panel" aria-label="Completion notification settings">
        <header className="settings-panel-header">
          <h2>Tentacle completion sound</h2>
          <p>Play a notification when a tentacle moves from processing to idle.</p>
        </header>
        <div className="settings-sound-picker">
          {TERMINAL_COMPLETION_SOUND_OPTIONS.map((option) => (
            <button aria-pressed={terminalCompletionSound === option.id} className="settings-sound-option" data-active={terminalCompletionSound === option.id ? "true" : "false"} key={option.id} onClick={() => { onTerminalCompletionSoundChange(option.id); onPreviewTerminalCompletionSound(option.id); }} type="button">
              <span className="settings-sound-option-label">{option.label}</span>
              <span className="settings-sound-option-description">{option.description}</span>
            </button>
          ))}
        </div>
        <div className="settings-panel-actions">
          <ActionButton aria-label="Preview selected completion sound" className="settings-sound-preview" onClick={() => { onPreviewTerminalCompletionSound(terminalCompletionSound); }} size="dense" variant="accent">Preview</ActionButton>
          <span className="settings-saved-pill">Saved to workspace</span>
        </div>
      </section>

      <section className="settings-panel" aria-label="Workspace surface visibility settings">
        <header className="settings-panel-header">
          <h2>Workspace surface visibility</h2>
          <p>Enable ou desabilite painéis do Dashboard.</p>
        </header>
        <div className="settings-toggle-grid">
          <SettingsToggle label="Trends Monitor" description="Notícias do Google e YouTube" ariaLabel="Enable Trends Monitor" checked={isMonitorVisible} onChange={onMonitorVisibilityChange} />
          <SettingsToggle label="Runtime status strip" description="Barra superior de status" ariaLabel="Show runtime status strip" checked={isRuntimeStatusStripVisible} onChange={onRuntimeStatusStripVisibilityChange} />
        </div>
      </section>
    </section>
  );
};
