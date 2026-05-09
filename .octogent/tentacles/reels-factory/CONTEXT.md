# Fábrica de Reels

## Scope
Transforma vídeos do YouTube em roteiros e transcrições otimizadas para Reels.

## Key Files
- `mcp_servers/reels-factory/server.py` — servidor MCP
- `scripts/new_tentacle.py` — como este tentáculo foi criado

## MCP Server
- `mcp_servers/reels-factory/server.py` — servidor MCP FastMCP
- Registrado em `.claude/settings.local.json` como `reels-factory`

## Ferramentas MCP disponíveis
- `reels-factory:process_youtube_video(url, language)` — Baixa e transcreve vídeos do YouTube (via Groq Whisper)

## Key Decisions
- Utilizar Whisper Large v3 via Groq para alta velocidade.
- Download via yt-dlp usando python -m para compatibilidade Windows.
- Suporte a .m4a para eliminar dependência de FFmpeg.

## Conventions
- Manter transcrições em `outputs/transcripts/`.

## Related Tentacles
- `orchestrator` — coordenador principal
