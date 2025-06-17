# backend/ai/ai_guardian.py

import openai
import os
from dotenv import load_dotenv

# Laster miljøvariabler fra .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔍 Funksjon som analyserer meldingen
def analyser_melding(melding):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du er en AI som vurderer meldinger for svindel eller trygghet. "
                                              "Svar alltid som et JSON-objekt med nøklene 'kategori' og 'forklaring'."},
                {"role": "user", "content": melding}
            ]
        )
        svar = response.choices[0].message.content.strip()

        # Tving GPT til å returnere gyldig JSON
        if svar.startswith('{') and 'kategori' in svar:
            import json
            parsed = json.loads(svar)
            return {
                "kategori": parsed.get("kategori", "ukjent"),
                "forklaring": parsed.get("forklaring", "Ingen forklaring.")
            }
        else:
            return {
                "kategori": "ukjent",
                "forklaring": svar
            }

    except Exception as e:
        print("❌ FEIL I AI:", e)
        return {
            "kategori": "feil",
            "forklaring": "AI-feil: " + str(e)
        }
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
