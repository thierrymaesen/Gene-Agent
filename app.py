# app.py
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

st.set_page_config(page_title="Gene-Agent | CSI Génomique", page_icon="🧬", layout="wide")

st.title("🧬 Gene-Agent : Assistant Génomique Autonome")
st.markdown("""
Posez une question impliquant de l'ADN. L'IA dispose de **deux outils** :
1. Un traducteur d'ADN en Protéines.
2. Une connexion à la base de données des espèces (Humain, Chien, Tardigrade...).
""")

# [VOTRE CODE ACTUEL DEMANDANT LA CLÉ API]
api_key = st.sidebar.text_input("Clé API Hugging Face (type Read) :", type="password")
st.sidebar.markdown("[Créer une clé gratuitement](https://huggingface.co/settings/tokens)")

# --- NOUVEAU BLOC : EXPLICATION DE L'ARCHITECTURE ---
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Architecture (Note Technique)")
st.sidebar.info("""
**Mode Démonstration :**
Cet agent autonome est actuellement connecté à une **base de données locale hautement optimisée**. 
Cela garantit un temps de réponse en millisecondes pour l'expérience utilisateur.

*Dans un environnement de production (serveurs lourds), l'Agent 'Species Identifier' serait directement branché sur l'API publique américaine NCBI (BLAST). Une requête prendrait alors entre 1 et 5 minutes.*
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧪 Séquences de Test")
st.sidebar.markdown("Copiez-collez l'un de ces ADN pour voir l'Agent en action :")
st.sidebar.code("ATGGCCCTGTGGATGCGCCTCCTG", language="text")
st.sidebar.caption("☝️ Suspect n°1")
st.sidebar.code("ATGTTTGTTTTTCTTGTTTTA", language="text")
st.sidebar.caption("☝️ Échantillon BSL-4 (Bio-sécurité)")
st.sidebar.code("ATGGGATATACTAGTATGGGA", language="text")
st.sidebar.caption("☝️ Découverte paléontologique")

# --- 3. LES OUTILS DE L'IA ---

@tool
def ai_dna_translator(dna_sequence: str) -> str:
    """
    Traduit une séquence d'ADN en acides aminés (protéines).
    
    Args:
        dna_sequence: La séquence d'ADN composée des lettres A, C, T, G.
    """
    return translate_dna_to_protein(dna_sequence)

@tool
def ai_species_identifier(dna_sequence: str) -> str:
    """
    Cherche à quelle espèce vivante appartient cette séquence d'ADN.
    Utilise cet outil UNIQUEMENT si l'utilisateur veut identifier l'origine de l'ADN.
    
    Args:
        dna_sequence: La séquence d'ADN à analyser dans la base de données.
    """
    return identify_species(dna_sequence)

# --- 4. LOGIQUE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: J'ai trouvé cet ADN : ATGGCCCTGTGGATGCGCCTCCTG. À qui appartient-il ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("Veuillez entrer votre clé API Hugging Face.")
        st.stop()
        
    os.environ["HUGGINGFACE_API_KEY"] = api_key
    
    # Utilisation du modèle importé dynamiquement
    model = HFModel(
        model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
        token=api_key
    )
    
        # 1. On définit nos règles strictes
    regles_strictes = """
    RÈGLES ABSOLUES POUR CETTE ANALYSE :
    1. Tu es l'IA principale du laboratoire de la police scientifique (CSI).
    2. Si on te demande d'identifier une espèce, utilise l'outil 'ai_species_identifier'.
    3. NE DEVINE JAMAIS l'espèce. Si l'outil te dit "Trop court" ou "Inconnu", tu dois dire la vérité à l'utilisateur. Tu as interdiction d'inventer un animal.
    4. Si on te demande de traduire, utilise l'outil 'ai_dna_translator' et explique les lettres trouvées.
    5. Adopte un ton professionnel, scientifique, et direct, comme un rapport de laboratoire.
    """
    
    # 2. On crée l'Agent normalement (SANS l'argument system_prompt qui cause l'erreur)
    agent = ToolCallingAgent(
        tools=[ai_dna_translator, ai_species_identifier], 
        model=model
    )

    with st.chat_message("assistant"):
        with st.expander("🧠 Voir les étapes d'investigation de l'Agent", expanded=True):
            status_text = st.empty()
            status_text.info("Investigation en cours...")
            try:
                # 3. On combine la question de l'utilisateur AVEC nos règles strictes
                mission_complete = f"{regles_strictes}\n\nVoici la demande de l'utilisateur :\n{prompt}"
                
                # On lance l'agent avec la mission complète
                reponse_finale = agent.run(mission_complete)
                status_text.success("Analyse terminée.")
            except Exception as e:
                reponse_finale = f"Erreur système : {str(e)}"
                status_text.error("Échec de l'analyse.")

        st.markdown("### 🔬 Rapport de Laboratoire :")
        st.markdown(reponse_finale)
        
    st.session_state.messages.append({"role": "assistant", "content": reponse_finale})