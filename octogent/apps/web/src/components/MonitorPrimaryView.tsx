import { useEffect, useState } from "react";
import { ActionButton } from "./ui/ActionButton";

type MonitorPrimaryViewProps = {
  monitorRuntime: {
    monitorConfig: any;
    monitorFeed: any;
    monitorError: string | null;
    isRefreshingMonitorFeed: boolean;
    isSavingMonitorConfig: boolean;
    refreshMonitorFeed: () => void;
    patchMonitorConfig: (patch: any) => Promise<boolean>;
  };
};

export const MonitorPrimaryView = ({ monitorRuntime }: MonitorPrimaryViewProps) => {
  const { monitorFeed, refreshMonitorFeed, patchMonitorConfig, isRefreshingMonitorFeed } = monitorRuntime;
  const [newTerm, setNewTerm] = useState("");

  const handleAddTerm = () => {
    if (!newTerm.trim()) return;
    const currentTerms = monitorFeed.queryTerms || [];
    if (!currentTerms.includes(newTerm.trim())) {
      patchMonitorConfig({ queryTerms: [...currentTerms, newTerm.trim()] });
    }
    setNewTerm("");
  };

  const handleRemoveTerm = (term: string) => {
    const nextTerms = (monitorFeed.queryTerms || []).filter((t: string) => t !== term);
    patchMonitorConfig({ queryTerms: nextTerms });
  };

  return (
    <section className="monitor-view" aria-label="Trends Intelligence Monitor">
      <header className="monitor-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', borderBottom: '1px solid #333' }}>
        <div>
          <h2 style={{ margin: 0, fontSize: '1.2rem', color: '#fff' }}>Trends-Intelligence</h2>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#888' }}>Monitoramento global de notícias via Google News</p>
        </div>
        <ActionButton onClick={refreshMonitorFeed} size="dense" variant="accent" disabled={isRefreshingMonitorFeed}>
          {isRefreshingMonitorFeed ? "Buscando..." : "Atualizar Agora"}
        </ActionButton>
      </header>

      <div className="monitor-content" style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '1rem', padding: '1rem', height: 'calc(100% - 70px)' }}>
        {/* LISTA DE NOTÍCIAS */}
        <section className="monitor-feed-panel" style={{ background: '#0a0a0a', border: '1px solid #222', borderRadius: '8px', overflowY: 'auto' }}>
          <header style={{ padding: '0.75rem', borderBottom: '1px solid #222', background: '#111', fontSize: '0.9rem', fontWeight: 'bold' }}>
            ÚLTIMAS NOTÍCIAS (GOOGLE NEWS)
          </header>
          <div className="feed-list">
            {monitorFeed.posts && monitorFeed.posts.length > 0 ? (
              monitorFeed.posts.map((post: any) => (
                <div key={post.id} style={{ padding: '1rem', borderBottom: '1px solid #111' }}>
                  <div style={{ fontSize: '0.75rem', color: '#4caf50', marginBottom: '0.3rem' }}>{post.author} • {new Date(post.createdAt).toLocaleString()}</div>
                  <a href={post.permalink} target="_blank" rel="noreferrer" style={{ color: '#eee', textDecoration: 'none', fontWeight: 500, fontSize: '1rem', display: 'block' }}>
                    {post.text}
                  </a>
                </div>
              ))
            ) : (
              <div style={{ padding: '2rem', textAlign: 'center', color: '#555' }}>Nenhuma notícia coletada ainda. Adicione termos de busca.</div>
            )}
          </div>
        </section>

        {/* CONFIGURAÇÃO DE TERMOS */}
        <section className="monitor-config-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ background: '#111', padding: '1rem', borderRadius: '8px', border: '1px solid #222' }}>
            <h3 style={{ fontSize: '0.9rem', marginTop: 0, marginBottom: '1rem' }}>TERMOS DE BUSCA</h3>
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
              <input 
                type="text" 
                value={newTerm} 
                placeholder="Ex: n8n, DeepSeek..."
                style={{ flex: 1, background: '#000', color: '#fff', border: '1px solid #333', padding: '0.5rem', borderRadius: '4px' }}
                onChange={(e) => setNewTerm(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddTerm()}
              />
              <button onClick={handleAddTerm} style={{ background: '#444', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '4px', cursor: 'pointer' }}>ADD</button>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {(monitorFeed.queryTerms || []).map((term: string) => (
                <span key={term} style={{ background: '#222', color: '#aaa', padding: '0.2rem 0.6rem', borderRadius: '12px', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  {term}
                  <span onClick={() => handleRemoveTerm(term)} style={{ cursor: 'pointer', color: '#f44336', fontWeight: 'bold' }}>×</span>
                </span>
              ))}
            </div>
          </div>

          <div style={{ background: '#111', padding: '1rem', borderRadius: '8px', border: '1px solid #222', fontSize: '0.8rem', color: '#777' }}>
            <strong>Status do Robô:</strong><br />
            Última atualização: {monitorFeed.lastFetchedAt ? new Date(monitorFeed.lastFetchedAt).toLocaleTimeString() : 'Nunca'}<br />
            Intervalo: 2 horas
          </div>
        </section>
      </div>
    </section>
  );
};
