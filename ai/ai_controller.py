from ai_guardian_beta import analyser_melding as guardian_ai
from agent_guardian import analyser_melding as gpt_ai

def velg_agent(melding: str) -> dict:
    m = melding.lower()

    if any(x in m for x in ["vipps", "bank", "phishing", "konto", "dnb", "svindel"]):
        print("🔐 Dirigerer til guardian_ai (med treningsdata)")
        return guardian_ai(melding)

    print("🧠 Dirigerer til gpt_ai")
    return gpt_ai(melding)