# constants.py
# reference pour ces constantes : https://www.ecologie.gouv.fr/sites/default/files/documents/Comite_scientfique_observation_loyers_annexe_abreviations_noms_voie.pdf
import re
import unidecode as _unidecode
import pandas as pd

TYPE_VOIE_ABBR_OFFICIAL = {
    "AERD": "AERODROME",
    "AERG": "AEROGARE",
    "ALL": "ALLEE",
    "A": "AUTOROUTE",
    "AV": "AVENUE",
    "BALC": "BALCON",
    "BRG": "BARRAGE",
    "BARR": "BARRIERE",
    "BASS": "BASSIN",
    "BOIS": "BOIS",
    "BD": "BOULEVARD",
    "BUTT": "BUTTE",
    "CARR": "CARREFOUR",
    "CAS": "CASERNE",
    "CCAL": "CENTRE COMMERCIAL",
    "CHAL": "CHALET",
    "CHP": "CHAMP",
    "CHAT": "CHATEAU",
    "CHAU": "CHAUSSEE",
    "CHEM": "CHEMIN",
    "CD": "CHEMIN DEPARTEMENTAL",
    "CITE": "CITE",
    "CLR": "CLAIRIERE",
    "CLIM": "CLIMAT",
    "CLOS": "CLOS",
    "CONT": "CONTOUR",
    "COTE": "CETE",
    "COTT": "COTTAGE",
    "CR": "COUR",
    "CRS": "COURS",
    "DOM": "DOMAINE",
    "ECL": "ECLUSE",
    "ESC": "ESCALIER",
    "ESP": "ESPLANADE",
    "ETG": "ETANG",
    "FBG": "FAUBOURG",
    "FERM": "FERME",
    "FOND": "FOND",
    "FONT": "FONTAINE",
    "FRT": "FORET",
    "FORT": "FORT",
    "FOSS": "FOSSE",
    "GAL": "GALERIE",
    "GARE": "GARE",
    "GDAV": "GRANDE AVENUE",
    "GDPL": "GRANDE PLACE",
    "GDR": "GRANDE RUE",
    "GRGE": "GRANGE",
    "HAM": "HAMEAU",
    "HIPP": "HIPPODROME",
    "ILE": "ILE",
    "IMP": "IMPASSE",
    "JARD": "JARDIN",
    "LDT": "LIEU DIT",
    "LOT": "LOTISSEMENT",
    "MAIL": "MAIL",
    "MAIS": "MAISON",
    "MCH": "MARCHE",
    "MARE": "MARE",
    "METR": "METRO",
    "MONT": "MONT",
    "MNT": "MONTEE",
    "PAL": "PALAIS",
    "PARC": "PARC",
    "PKG": "PARKING",
    "PARV": "PARVIS",
    "PASS": "PASSAGE",
    "PAV": "PAVILLON",
    "PEL": "PELOUSE",
    "PTR": "PETITE RUE",
    "PIEC": "PIECE",
    "PL": "PLACE",
    "PLAI": "PLAINE",
    "PK": "POINT KILOMETRIQUE",
    "PNTE": "POINTE",
    "PONT": "PONT",
    "PORT": "PORT",
    "PRTE": "PORTE",
    "PRAI": "PRAIRIE",
    "PRE": "PRE",
    "PROM": "PROMENADE",
    "QUAI": "QUAI",
    "QUAR": "QUARTIER",
    "RPE": "RAMPE",
    "RER": "RER",
    "RES": "RESIDENCE",
    "RDPT": "ROND POINT",
    "RTE": "ROUTE",
    "RD": "ROUTE DEPARTEMENTALE",
    "RN": "ROUTE NATIONALE",
    "RUE": "RUE",
    "RLE": "RUELLE",
    "SENT": "SENTIER",
    "SQ": "SQUARE",
    "ST": "STATION",
    "TERR": "TERRASSE",
    "TOUR": "TOUR",
    "TRAV": "TRAVERSE",
    "VALL": "VALLEE",
    "VEN": "VENELLE",
    "VLA": "VILLA",
    "VOIE": "VOIE",
    "VC": "VOIE COMMUNALE",
    "ZA": "ZONE ARTISANALE",
    "ZI": "ZONE INDUSTRIELLE",
    "VCHE" : "VIEUX CHEMIN",
}

TYPES_VOIE = sorted([
    "ALLEE", "ANCIEN CHEMIN", "AVENUE", "BOULEVARD", "CHEMIN", "CITE", "COUR",
    "CHAUSSEE", "CARREFOUR", "CLOS", "DOMAINE", "ECOLE", "ESPLANADE",
    "GRANDE RUE", "HAMEAU", "IMPASSE", "PASSAGE", "PLACE", "PONT",
    "PORTE", "PROMENADE", "QUAI", "RESIDENCE", "RUE", "ROUTE", "RUELLE", "SQUARE",
    "SENTE", "SENTIER", "TERRASSE", "VILLA", "VOIE", "ZONE", "ZA", "VC", "VIL", "VLA"
], key=len, reverse=True)  # trie du plus long au plus court

# (optionnel) Libellé complet -> Abréviation (utile si tu veux re-compresser ensuite)
TYPE_VOIE_FULL_TO_ABBR = {v: k for k, v in TYPE_VOIE_ABBR_OFFICIAL.items()}

# Alias pour rattraper les variantes / fautes fréquentes rencontrées dans les données
# (tes exemples inclus : CAR, CHE, GR, HAM, IMP, PAS, PCH, PTE, RLE, RPT, SEN, SQ, VC, VIL, VLA, ZA…)
# Clés = ce qu’on voit en base après normalisation ; Valeur = abréviation canonique officielle.
TYPE_VOIE_ABBR_ALIASES = {
    "CHE": "CHEM",      # CHE → CHEM (CHEMIN)
    "CAR": "CARR",      # CAR → CARR (CARREFOUR)
    "PAS": "PASS",      # PASSAGE
    "RPT": "RDPT",      # ROND-POINT (souvent saisi sans le D)
    "SEN": "SENT",      # SENTIER
    "PTE": "PRTE",      # PORTE (PTE très courant)
    "VIL": "VLA",       # VILLA (souvent tronqué en VIL)
    "VC.": "VC",
    "AV.": "AV",
    "BD.": "BD",  # avec point
    "ETANG": "ETG",     # quand l’abréviation est remplacée par le mot sans accents
    "ECLUSE": "ECL",
    "METRO": "METR",
    "RESIDENCE": "RES",
    "RONDPOINT": "RDPT",
    "MTE" : "MTN",
    "PLE" : "PL",
    # Ambiguïtés qu’on préfère NE PAS corriger automatiquement :
    # "GR" : peut vouloir dire GARE, GRANGE (GRGE), GRANDE RUE (GDR)…
    # "PCH": non officiel dans la liste (parfois "PORCHE", non présent dans l’annexe)
}

# --- Helpers de normalisation/correction ---

def _normalize_abbr(raw: str) -> str:
    """
    Normalise ce qu'on lit dans 'type_de_voie' :
    - supprime accents, points, tirets, espaces
    - majuscules
    """
    if raw is None:
        return ""
    x = _unidecode.unidecode(str(raw)).upper()
    x = re.sub(r"[.\-\s/']", "", x)  # enlève ., -, espaces, /, '
    return x

def abbr_to_full(value: str) -> str:
    """
    Convertit une abréviation (même mal saisie) vers le libellé complet.
    Si non reconnu, renvoie la valeur d’origine.
    """
    if value is None:
        return value
    norm = _normalize_abbr(value)
    canon = TYPE_VOIE_ABBR_ALIASES.get(norm, norm)  # corrige CHE→CHEM, RPT→RDPT, etc.
    return TYPE_VOIE_ABBR_OFFICIAL.get(canon, value)

def expand_type_de_voie_column(series):
    """
    À utiliser sur la colonne pandas 'type_voie' (ou 'type_de_voie').
    """
    return series.map(abbr_to_full)

def detect_type_in_voie(row):
    voie = str(row["voie"]).strip()
    for t in TYPES_VOIE:
        if voie.upper().startswith(t):
            # si type_voie vide ou générique, on le remplace
            if pd.isna(row["type_voie"]) or row["type_voie"].strip() == "":
                row["type_voie"] = t
            else:
                # concat si besoin ("RUE" + "GRANDE RUE" -> garder le plus pertinent)
                row["type_voie"] = t
            # on supprime la partie trouvée au début de "voie"
            row["voie"] = voie[len(t):].strip()
            break
    return row