import os
import json
from pathlib import Path
import yt_dlp
from groq import Groq
from dotenv import load_dotenv

# Load env
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DOWNLOAD_DIR = ROOT_DIR / "outputs" / "temp_audio"
TRANSCRIPT_DIR = ROOT_DIR / "outputs" / "transcripts"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

def process_video(url):
    print(f"Processing: {url}")
    
    # Get Info
    ydl_opts_info = {'quiet': True, 'no_warnings': True, 'nocheckcertificate': True}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title")
        print(f"Title: {title}")

    # Download
    output_template = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
    ydl_opts_dl = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        print(f"Downloaded to: {file_path}")

    # Transcribe
    print(f"Transcribing: {file_path}")
    with open(file_path, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model="whisper-large-v3",
            response_format="text",
            language="pt"
        )
    
    # Save Transcript
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '.', '_')]).rstrip()
    transcript_file = TRANSCRIPT_DIR / f"transcricao_{safe_title}.txt"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    
    print(f"Saved transcript to: {transcript_file}")
    return title, transcription

if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/watch?v=F0S_O4C_Lmo",
        "https://www.youtube.com/watch?v=v2S_6J8Z02Y",
        "https://www.youtube.com/watch?v=f9vT89eMshQ"
    ]
    
    all_transcripts = []
    for url in urls:
        try:
            title, transcript = process_video(url)
            all_transcripts.append({"title": title, "transcript": transcript})
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    # Save a summary for script generation
    with open(ROOT_DIR / "outputs" / "all_transcripts.json", "w", encoding="utf-8") as f:
        json.dump(all_transcripts, f, ensure_ascii=False, indent=2)
