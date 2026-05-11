
import os
import json
import uuid
from datetime import datetime

GEMINI_DIR = r"C:\Users\gdesi\.gemini\tmp\tentacles-ai\chats"
DASH_DIR = r"C:\Users\gdesi\.octogent\projects\6db28e03-c46a-44da-8f55-7236cda76706\state\transcripts"

def sync():
    if not os.path.exists(DASH_DIR):
        os.makedirs(DASH_DIR, exist_ok=True)

    # 1. Processar Gemini -> Dashboard
    if os.path.exists(GEMINI_DIR):
        gemini_files = [f for f in os.listdir(GEMINI_DIR) if f.endswith(".jsonl") and not f.startswith("dash-")]
        print(f"Sincronizando {len(gemini_files)} chats do Gemini...")
        for filename in gemini_files:
            file_path = os.path.join(GEMINI_DIR, filename)
            session_id = "gemini-" + filename.replace(".jsonl", "")
            
            dest_jsonl = os.path.join(DASH_DIR, f"{session_id}.jsonl")
            dest_turns = os.path.join(DASH_DIR, f"{session_id}.claude-turns.json")
            
            turns = []
            first_ts = None
            last_ts = None
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            ts = data.get("timestamp") or data.get("startTime") or data.get("lastUpdated")
                            if ts:
                                last_ts = ts
                                if not first_ts: first_ts = ts
                            
                            if data.get("type") in ["user", "gemini"]:
                                role = "user" if data["type"] == "user" else "assistant"
                                content = ""
                                raw = data.get("content", "")
                                if isinstance(raw, list):
                                    content = " ".join([c.get("text", "") for c in raw if isinstance(c, dict) and "text" in c])
                                elif isinstance(raw, str): content = raw
                                
                                if role == "assistant" and not content:
                                    if data.get("thoughts"): content = data["thoughts"][0].get("description", "(Pensando...)")
                                    elif data.get("toolCalls"): content = "(Executando ferramentas...)"
                                
                                if content:
                                    turns.append({"turnId": data.get("id", str(uuid.uuid4())), "role": role, "content": content, "startedAt": ts or datetime.now().isoformat()})
                        except: continue
                
                if turns:
                    with open(dest_turns, 'w', encoding='utf-8') as f: json.dump(turns, f, indent=2)
                    with open(dest_jsonl, 'w', encoding='utf-8') as f:
                        f.write(json.dumps({"type": "session_start", "eventId": str(uuid.uuid4()), "sessionId": session_id, "tentacleId": "__OCTOBOSS__", "timestamp": first_ts or datetime.now().isoformat()}) + "\n")
                        f.write(json.dumps({"type": "session_end", "eventId": str(uuid.uuid4()), "sessionId": session_id, "tentacleId": "__OCTOBOSS__", "timestamp": last_ts or datetime.now().isoformat(), "reason": "session_close"}) + "\n")
            except Exception as e: print(f"Erro em {filename}: {e}")

    # 2. Indexar sessões nativas do Dashboard que estão "órfãs"
    dash_files = [f for f in os.listdir(DASH_DIR) if f.endswith(".jsonl") and not f.startswith("gemini-")]
    print(f"Indexando {len(dash_files)} sessões nativas do Dashboard...")
    for filename in dash_files:
        session_id = filename.replace(".jsonl", "")
        dest_turns = os.path.join(DASH_DIR, f"{session_id}.claude-turns.json")
        
        # if os.path.exists(dest_turns): continue # Opcional: pular se já existe
        
        file_path = os.path.join(DASH_DIR, filename)
        turns = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        ts = data.get("timestamp") or datetime.now().isoformat()
                        if data.get("type") == "user_prompt_submit":
                            turns.append({"turnId": data.get("eventId", str(uuid.uuid4())), "role": "user", "content": data.get("prompt", ""), "startedAt": ts})
                        elif data.get("type") == "agent_response":
                            turns.append({"turnId": data.get("eventId", str(uuid.uuid4())), "role": "assistant", "content": data.get("content", ""), "startedAt": ts})
                    except: continue
            if turns:
                with open(dest_turns, 'w', encoding='utf-8') as f: json.dump(turns, f, indent=2)
        except Exception as e: print(f"Erro em {filename}: {e}")

    print("Consolidacao concluida!")

if __name__ == "__main__":
    sync()
