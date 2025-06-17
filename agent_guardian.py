import openai
import os
from dotenv import load_dotenv

# 🔑 Laster miljøvariabler fra .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Funksjon som analyserer meldingen med GPT
def analyser_melding(melding: str) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du er en AI som vurderer meldinger for svindel, trygghet eller trusler. Svar alltid i format: Kategori: <kategori>. Forklaring: <forklaring>."},
                {"role": "user", "content": melding}
            ],
            max_tokens=100
        )

        svar = response.choices[0].message.content.strip()

        # 🧪 Prøver å splitte ut kategori og forklaring fra GPT
        linjer = svar.split("\n")
        kategori = "ukjent"
        forklaring = svar

        for linje in linjer:
            if "kategori" in linje.lower():
                kategori = linje.split(":")[-1].strip()
            elif "forklaring" in linje.lower():
                forklaring = linje.split(":")[-1].strip()

        return {
            "kategori": kategori or "ukjent",
            "forklaring": forklaring or "Ingen forklaring"
        }

    except Exception as e:
        print("FEIL I AI:", e)
        return {
            "kategori": "feil",
            "forklaring": "AI-feil: " + str(e)
        }