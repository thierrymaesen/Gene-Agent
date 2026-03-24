# agent_test.py
import streamlit as st
import os
from bio_tools import translate_dna_to_protein, identify_species

# --- GESTION ROBUSTE DE L'IMPORT DE SMOLAGENTS ---
from smolagents import ToolCallingAgent, tool

try:
    # Pour les versions récentes de smolagents (sur Streamlit Cloud)
    from smolagents import InferenceClientModel as HFModel
except ImportError:
    try:
        # Pour les versions intermédiaires
        from smolagents import HfApiModel as HFModel
    except ImportError:
        # Pour les anciennes versions avec litellm
        from smolagents import LiteLLMModel as HFModel
# -------------------------------------------------

# 1. Le "Décorateur" @tool
@tool
def ai_dna_translator(dna_sequence: str) -> str:
    """
    Traduit une séquence d'ADN en acides aminés (protéines).
    Utilise cet outil lorsque l'utilisateur te demande de traduire, décoder ou analyser de l'ADN.
    
    Args:
        dna_sequence: La séquence d'ADN composée des lettres A, C, T, G (ex: 'ATGGCC').
    """
    return translate_dna_to_protein(dna_sequence)

# 2. Configuration du Cerveau 
# REMPLACEZ par votre vraie clé Hugging Face (type Read) !
os.environ["HUGGINGFACE_API_KEY"] = "VOTRE_CLE_ICI" 

print("🧠 Initialisation du cerveau de l'Agent...")
model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=os.environ.get("HUGGINGFACE_API_KEY", "CLE_TEST")
)

# 3. Création de l'Agent
agent = ToolCallingAgent(tools=[ai_dna_translator], model=model)

# --- TEST DE L'AGENT ---
if __name__ == "__main__":
    print("🤖 Agent prêt ! Envoi de la mission...")
    print("-" * 40)
    
    mission = "Un biologiste m'a envoyé cette séquence d'ADN : 'ATGGCCATTTAA'. Peux-tu la traduire en protéines pour moi et m'expliquer brièvement ce qu'est une protéine ?"
    
    # L'Agent s'exécute
    reponse = agent.run(mission)
    
    print("\n" + "=" * 40)
    print("🎯 RÉPONSE FINALE DE L'IA :")
    print(reponse)