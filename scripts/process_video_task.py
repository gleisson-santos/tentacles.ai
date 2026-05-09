import os
import sys
import json
from pathlib import Path
import yt_dlp
from groq import Groq
from dotenv import load_dotenv

# Configurações de caminhos
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Pastas
DOWNLOAD_DIR = ROOT_DIR / "outputs" / "temp_audio"
TRANSCRIPT_DIR = ROOT_DIR / "outputs" / "transcripts"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

def get_video_info(url):
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def download_audio(url):
    output_template = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def transcribe(file_path):
    with open(file_path, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model="whisper-large-v3",
            response_format="text",
            language="pt"
        )
        return transcription

def generate_viral_script(transcript):
    prompt = f"""
Você é um especialista em marketing viral para Reels e TikTok.
Com base na transcrição abaixo, crie um roteiro viral (30-60 segundos).

REGRAS:
1. Gancho forte nos primeiros 3 segundos.
2. Linguagem dinâmica e envolvente.
3. Inclua indicações visuais (Visual Cues).
4. Termine com um CTA claro.

Transcrição:
{transcript}
"""
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def main():
    url = "https://www.youtube.com/watch?v=f9vT89eMshQ"
    print(f"Processando vídeo: {url}")
    
    try:
        info = get_video_info(url)
        video_title = info.get("title", "video_sem_titulo").replace(" ", "_").replace("/", "-")
        print(f"Título: {info.get('title')}")
        
        print("Baixando áudio...")
        audio_file = download_audio(url)
        print(f"Áudio salvo em: {audio_file}")
        
        print("Transcrevendo...")
        transcript = transcribe(audio_file)
        
        transcript_file = TRANSCRIPT_DIR / f"{video_title}_transcription.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcrição salva em: {transcript_file}")
        
        print("Gerando roteiro viral...")
        viral_script = generate_viral_script(transcript)
        
        script_file = TRANSCRIPT_DIR / f"{video_title}_viral_script.md"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(viral_script)
        print(f"Roteiro viral salvo em: {script_file}")
        
        print("\n=== ROTEIRO VIRAL ===\n")
        print(viral_script)
        print("\n=====================\n")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
