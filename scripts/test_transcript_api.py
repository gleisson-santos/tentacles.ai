from youtube_transcript_api import YouTubeTranscriptApi
import json

video_id = 'f9vT89eMshQ'

try:
    print(f"Listando transcrições para {video_id}...")
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    # Tenta encontrar em português, senão inglês, senão a primeira disponível
    try:
        transcript = transcript_list.find_transcript(['pt'])
    except:
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            transcript = next(iter(transcript_list))
            
    print(f"Transcrição encontrada: {transcript.language} ({transcript.language_code})")
    data = transcript.fetch()
    
    full_text = " ".join([item['text'] for item in data])
    print("\nTexto completo:")
    print(full_text[:500] + "...")
    
    with open("outputs/transcripts/transcript_api_result.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
except Exception as e:
    print(f"Erro: {str(e)}")
