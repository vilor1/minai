import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ⚠️ COLOQUE SUA CHAVE AQUI (não recomendado em produção)
GROQ_API_KEY = "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"

GROQ_API_URL = "https://api.groq.com/openai/v1/responses"

@app.get("/npc")
def npc(msg: str):
    prompt = f"""
Você é um NPC de Minecraft Education Edition.
Responda APENAMENTE usando comandos no formato:

SAY: <texto>
MOVE: <forward|back|left|right>
ATTACK: <entity>
COLLECT: <item>
DEFEND: <entity>
INTERACT: <action>

Jogador disse:
{msg}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-20b",  # ou outro modelo disponível do Groq
        "input": prompt
    }

    try:
        r = requests.post(GROQ_API_URL, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        
        # a saída costuma estar em "output_text"
        reply = data.get("output_text") or ""
        if not reply:
            raise HTTPException(status_code=500, detail="Resposta vazia da Groq")
        
        return {"reply": reply.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
