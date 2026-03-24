# bio_tools.py
from Bio.Seq import Seq
import re

def validate_dna_sequence(sequence: str) -> bool:
    clean_seq = sequence.upper().replace(" ", "")
    if re.fullmatch(r"^[ACTG]+$", clean_seq):
        return True
    return False

def translate_dna_to_protein(dna_sequence: str) -> str:
    clean_seq = dna_sequence.upper().replace(" ", "")
    if not validate_dna_sequence(clean_seq):
        return "Erreur : Séquence invalide."
    
    try:
        dna_obj = Seq(clean_seq)
        protein_seq = dna_obj.translate(to_stop=True)
        return str(protein_seq)
    except Exception as e:
        return f"Erreur lors de la traduction : {str(e)}"

def identify_species(dna_sequence: str) -> str:
    """
    Cherche l'ADN dans la base de données locale (Mode Démo) pour identifier l'espèce.
    """
    clean_seq = dna_sequence.upper().replace(" ", "")
    
    if len(clean_seq) < 12:
        return "Erreur_Scientifique : La séquence est trop courte (moins de 12 nucléotides). Impossible d'identifier une espèce de manière fiable."
    
    # Base de données de Démonstration (Séquences célèbres / Easter Eggs)
    database = {
        # Humain
        "ATGGCCCTGTGGATGCGCCTCCTG": "Homo sapiens (Humain) - Gène de l'Insuline, essentiel à la régulation du sucre.",
        "ATGCGTAAGGAGAAGTACGGA": "Homo sapiens (Humain) - Allèle de l'œil bleu (gène OCA2).",
        
        # Animaux Extrêmes
        "ATGGATCATGCAGCAAATCGT": "Ramazzottius varieornatus (Tardigrade) - Gène Dsup, confère la résistance aux radiations extrêmes.",
        
        # Animaux Préhistoriques (Reconstitués/Estimés)
        "ATGGCAGCAGCTGCAGCTACA": "Mammuthus primigenius (Mammouth Laineux) - Gène de l'hémoglobine adaptée au froid extrême.",
        "ATGGGATATACTAGTATGGGA": "Tyrannosaurus rex - Fragment de collagène osseux (estimé via phylogénie aviaire).",
        
        # Virus et Pathogènes célèbres
        "ATGTTTGTTTTTCTTGTTTTA": "SARS-CoV-2 (Coronavirus) - Début de la protéine Spike (Glycoprotéine de surface).",
        "ATGGGCGGTGCTGCCTGT": "Virus Ebola (Ebolavirus Zaire) - Début de la nucléoprotéine (NP).",
        
        # Plantes & Champignons
        "ATGGCTTCCTCTATGCTCTCT": "Coffea arabica (Caféier) - Gène impliqué dans la synthèse de la caféine.",
        "ATGGGCAAAGGTTCAACAAAG": "Amanita phalloides (Amanite phalloïde) - Séquence codant pour l'alpha-amanitine (toxine mortelle)."
    }
    
    # 3. Recherche de correspondance souple
    for known_seq, species in database.items():
        if clean_seq in known_seq or known_seq in clean_seq:
            return f"CORRESPONDANCE POSITIVE : {species}"
            
    return "RÉSULTAT NÉGATIF : Aucune correspondance trouvée dans la base de données LOCALE (Mode Démo). Pour une analyse complète, ce système devrait être branché sur l'API NCBI BLAST (temps de traitement estimé : 3 à 5 minutes)."