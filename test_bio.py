# test_bio.py
import pytest
from bio_tools import validate_dna_sequence, translate_dna_to_protein, identify_species

def test_validation_dna():
    # L'ADN normal doit passer
    assert validate_dna_sequence("ATGC") == True
    assert validate_dna_sequence("a t g c") == True
    # L'ADN pirate doit échouer
    assert validate_dna_sequence("ATGX") == False
    assert validate_dna_sequence("DROP TABLE") == False

def test_translation():
    # ATG GCA TAA = M A (et on s'arrête)
    assert translate_dna_to_protein("ATGGCATAA") == "MA"
    # Un mauvais ADN doit renvoyer une erreur
    assert "Erreur" in translate_dna_to_protein("ATGXXX")

def test_identification_length():
    # Une séquence trop courte doit être bloquée
    assert "Erreur_Scientifique" in identify_species("ATGC")

def test_identification_known():
    # Le Tardigrade doit être trouvé
    result = identify_species("ATGGATCATGCAGCAAATCGT")
    assert "Tardigrade" in result