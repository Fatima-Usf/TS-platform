# -*- coding: utf-8 -*-
FILIERE = (
    ("1", ("Mathematique")),
    ("2", ("Informatique")),
)


NIVEAU = (
    ("1", ("L1")),
    ("2", ("L2")),
    ("3", ("L3")),
    ("4", ("M1")),
    ("5", ("M2")),
)

GRADE = (
    ("0", "Mâitre assistant(e) A"),
    ("PROF", "Professeur"),
    ("2", "Mâitre conférence A"),
    ("3", "Mâitre conférence B"),
    ("4", "Mâitre assistant(e) B"),

)
SEXE = (
    ("1", ("M")),
    ("2", ("F")),
)

DOMAINE = (
    ("1", ("MI")),
)

"""
    Lister les status des étudiants
    TODO: à revoir avec les secretaires
"""
STATUS_DOSSIER = (
    ('0', 'Non comfirmé'),
    ('1', 'Inscrit'),
    ('2', 'Congé academique'),
    ('3', 'Exclus')
)

SESSION = [
    ('0', 'S1'),
    ('1', 'S2'),
]
