import os
import json
from dotenv import load_dotenv
import openai

# Last inn miljøvariabler fra .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Last inn treningsdata
with open("treningsdata_beta.json", encoding="utf-8") as f1:
    treningsdata_beta = json.load(f1)

with open("trening_falske_sider.json", encoding="utf-8") as f2:
    trening_falske_sider = json.load(f2)

alle_eksempler = treningsdata_beta + trening_falske_sider

def analyser_melding(melding: str) -> dict:
    melding = melding.lower().strip()

    # 1. Sjekk treningsdata først
    for eksempel in alle_eksempler:
        if eksempel["input"].lower() in melding:
            return {
                "kategori": eksempel["kategori"],
                "forklaring": eksempel["forklaring"]
            }

    # 2. Hvis ingen treff, bruk GPT som backup
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Du er en AI som vurderer meldinger for svindel eller trygghet."
                },
                {
                    "role": "user",
                    "content": melding
                }
            ]
        )

        svar = response.choices[0].message.content.strip()
        return {
            "kategori": "GPT",
            "forklaring": svar
        }

    except Exception as e:
        return {
            "kategori": "feil",
            "forklaring": "Ingen kontakt med server eller AI-feil: " + str(e)
        }