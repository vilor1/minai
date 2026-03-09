from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
app = FastAPI()

@app.get("/npc")
def npc(msg: str):
    prompt = f"""
Você é um NPC do Minecraft Education Edition.

Responda APENAMENTE usando comandos no formato:

SAY: <texto>
MOVE: <forward | back | left | right>

Não explique nada.

Jogador disse:
{msg}
"""

    try:
        response = model.generate_content(prompt)
        if not response.text:
            raise HTTPException(status_code=500, detail="Resposta vazia da IA")
        return {"reply": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
