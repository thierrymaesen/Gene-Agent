# agent_test.py
from smolagents import ToolCallingAgent, tool, LiteLLMModel
import os

# On importe notre fonction biologique sécurisée créée à l'étape 1
from bio_tools import translate_dna_to_protein

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
# Utilisation de LiteLLMModel qui est le standard actuel de smolagents pour appeler des API
model = LiteLLMModel(
    model_id="huggingface/Qwen/Qwen2.5-Coder-32B-Instruct",
    api_key=os.environ["HUGGINGFACE_API_KEY"]
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