# 🧬 Gene-Agent : IA Génomique Autonome (Agentic Workflow)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud_Deployed-red?logo=streamlit&logoColor=white)
![AI Framework](https://img.shields.io/badge/Framework-smolagents_(CodeAgent)-yellow)
![LLM](https://img.shields.io/badge/LLM-Qwen_2.5_Coder_32B-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![CI/CD](https://github.com/thierrymaesen/Gene-Agent/actions/workflows/ci.yml/badge.svg)

**Gene-Agent** est un système d'Intelligence Artificielle autonome conçu pour la bio-informatique. Contrairement aux chatbots classiques ou aux systèmes RAG, ce projet utilise un **Agentic Workflow** (Flux de travail Agentique), permettant au modèle de langage (LLM) de raisonner de manière autonome, de sélectionner et d'exécuter des outils Python sur mesure pour analyser des séquences d'ADN.

---

## 🚀 Le Concept : AI for Science

Ce projet démontre comment les Grands Modèles de Langage (LLMs) peuvent être équipés d'outils scientifiques déterministes pour éviter les "hallucinations" et fournir des résultats précis et vérifiables.

Lorsqu'un utilisateur soumet une séquence d'ADN, l'Agent :
1. **Raisonne** sur la demande (S'agit-il d'une traduction ? D'une identification ?).
2. **Sélectionne** l'outil approprié (`ai_dna_translator` ou `ai_species_identifier`).
3. **Exécute** le code Python/Biopython sous-jacent.
4. **Synthétise** le résultat déterministe sous la forme d'un "Rapport de Laboratoire / Scène de crime" complet.

## ⚙️ Architecture & Stack Technique

- **Le Cerveau (LLM)** : `Qwen/Qwen2.5-Coder-32B-Instruct` (via l'API d'inférence Hugging Face). Choisi pour ses excellentes capacités natives de "Function Calling" (Appel de fonctions).
- **L'Orchestrateur** : `smolagents` (Hugging Face). Un framework ultraléger et sécurisé pour construire des agents autonomes.
- **Les Outils** : Fonctions Python personnalisées utilisant `Biopython` pour garantir une rigueur scientifique absolue et assainir les entrées (via Regex).
- **L'Interface** : `Streamlit` pour une expérience utilisateur réactive en temps réel, permettant de visualiser le processus de raisonnement ("Thought Process") de l'Agent.

### ⚠️ Note sur la Base de Données (Mode Démo)
Afin de garantir des temps de réponse inférieurs à la seconde pour la démonstration utilisateur, l'outil `ai_species_identifier` est actuellement connecté à un dictionnaire local hautement optimisé contenant des séquences génétiques célèbres (Covid-19, T-Rex, Tardigrade, etc.). 
*Dans un environnement de production réel, cet outil serait remplacé par une requête vers l'API publique américaine NCBI BLAST (ce qui nécessite généralement 1 à 5 minutes de traitement par requête).*

## 🛠️ Installation Locale

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/VOTRE_PSEUDO/Gene-Agent.git
   cd Gene-Agent
   ```
2. Créer un environnement virtuel et installer les dépendances :
   ```bash
   python -m venv venv
   source venv/Scripts/activate # Sur Windows: .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```
3. Lancer l'application :
   ```bash
   streamlit run app.py
   ```
*(Note : Vous aurez besoin d'une clé API Hugging Face gratuite avec les permissions 'Read' pour faire fonctionner l'agent).*

## 🧪 Séquences de Test Rapide
Essayez ces séquences dans l'application pour voir l'Agent en action :
- `ATGGCCCTGTGGATGCGCCTCCTG` (Insuline Humaine)
- `ATGTTTGTTTTTCTTGTTTTA` (Protéine Spike du SARS-CoV-2)
- `ATGGGATATACTAGTATGGGA` (Collagène estimé du T-Rex)

## 🔒 Sécurité & Anti-Hallucination
Le système est construit avec des garde-fous stricts :
- **Sanitization des Entrées** : Les outils Python vérifient les entrées via Regex (`^[ACTG]+$`) avant traitement pour prévenir toute injection de prompt.
- **Prompting Système Strict** : L'Agent a pour instruction explicite de **ne jamais** deviner ou inventer une espèce si l'outil renvoie un résultat négatif ou si la séquence fait moins de 12 nucléotides.

---
*Créé pour démontrer l'application de l'IA Agentique au domaine de la Bio-informatique.*
---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**Thierry Maesen**
- **Projet** : [Gene-Agent GitHub Repository](https://github.com/thierrymaesen/Gene-Agent)
- **Concept** : Démonstration de l'architecture *Agentic Workflow* et *AI for Science*.

*Ce projet a été conçu pour illustrer la création d'Agents Autonomes sécurisés, résilients aux hallucinations, et déployés via un pipeline CI/CD professionnel.*