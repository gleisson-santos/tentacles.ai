# Contexto: Fábrica de Reels

Este agente é responsável por processar URLs do YouTube, extrair o áudio e gerar transcrições de alta qualidade usando o modelo Whisper Large v3 via Groq API.

## Objetivos
- Automatizar a extração de conteúdo de vídeos.
- Facilitar a criação de roteiros para Reels e Shorts.
- Garantir que o processo de download e transcrição seja rápido e resiliente.

## Ferramentas
- **yt-dlp**: Motor de download (usado via Python).
- **Groq Whisper**: API de transcrição ultra-rápida.

## Fluxo de Trabalho
1. Recebe URL.
2. Valida ID do vídeo.
3. Baixa melhor áudio disponível (geralmente .m4a).
4. Envia para Groq para transcrição.
5. Salva resultado em `outputs/transcripts/`.
6. Limpa arquivos temporários.
