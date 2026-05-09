import os
import re
import uuid
import logging
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from groq import Groq
from mcp.server.fastmcp import FastMCP

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("reels-factory")

# Carrega variáveis de ambiente
load_dotenv()

mcp = FastMCP("reels-factory")

def extract_video_id(url: str) -> str:
    """Extrai o ID do vídeo de diversas variantes de URL do YouTube."""
    parsed = urlparse(url)
    if parsed.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed.path[1:]
    if parsed.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        if parsed.path.startswith(('/embed/', '/v/', '/shorts/')):
            return parsed.path.split('/')[2]
    return None

@mcp.tool()
def process_youtube_video(url: str, language: str = None) -> dict:
    """
    Baixa o áudio de um vídeo do YouTube, transcreve usando Groq Whisper 
    e salva o resultado em um arquivo .txt.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return {"status": "error", "message": "URL do YouTube inválida."}

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    temp_id = str(uuid.uuid4())[:8]
    base_audio = f"temp_audio_{video_id}_{temp_id}"
    
    output_dir = Path("outputs/transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)
    transcript_file = output_dir / f"{video_id}.txt"

    try:
        logger.info(f"Iniciando download do áudio: {url}")
        
        # yt-dlp: baixa o melhor áudio disponível (geralmente .m4a ou .webm)
        # Groq suporta: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
        ydl_command = [
            "python", "-m", "yt_dlp",
            "-f", "bestaudio/best",
            "--no-playlist",
            "--socket-timeout", "30",
            "--retries", "3",
            "--output", f"{base_audio}.%(ext)s",
            url
        ]
        
        result = subprocess.run(ydl_command, check=True, capture_output=True, text=True)
        
        # Localiza o arquivo baixado (pode ser .m4a, .webm, etc)
        downloaded_files = list(Path(".").glob(f"{base_audio}.*"))
        if not downloaded_files:
             return {"status": "error", "message": "Falha no download do áudio."}
        
        audio_path = downloaded_files[0]
        logger.info(f"Arquivo baixado: {audio_path.name}. Enviando para Groq Whisper...")

        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_path.name, file.read()),
                model="whisper-large-v3",
                prompt="Transcrição de vídeo do YouTube para criação de conteúdo.",
                response_format="text",
                language=language
            )

        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcription)

        logger.info(f"Sucesso! Transcrição salva em {transcript_file}")
        
        return {
            "status": "success",
            "video_id": video_id,
            "path": str(transcript_file.absolute()),
            "transcript_preview": transcription[:500] + "..."
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Erro no yt-dlp: {e.stderr}")
        return {"status": "error", "message": f"Erro no download: {e.stderr}"}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        # Cleanup rigoroso de todos os arquivos temporários criados
        for extra in Path(".").glob(f"{base_audio}*"):
            try: os.remove(extra)
            except: pass

if __name__ == "__main__":
    mcp.run()
