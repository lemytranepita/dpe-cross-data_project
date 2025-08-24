import pandas as pd
import unidecode
import re

def nettoyer_texte(val: str) -> str:
    """Nettoyage d'un champ texte : accents, majuscules, tirets/apostrophes remplacés par espace."""
    if not isinstance(val, str):
        return ""
    val = unidecode.unidecode(val)  # enlever accents
    val = val.upper()  # majuscules
    val = val.replace("-", " ").replace("'", " ")  # tirets et apostrophes remplacés
    val = re.sub(r"\s+", " ", val).strip()  # espaces multiples
    return val

def extraire_depuis_adresse(adresse: str):
    """
    Exemple : '13Z RUE DE LA PREVOYANCE 01000 BOURG EN BRESSE'
    -> numero = '13Z'
    -> nom_rue = 'RUE DE LA PREVOYANCE'
    """
    if not adresse:
        return "", ""

    adresse = nettoyer_texte(adresse)

    # Regex pour capturer : numero (ex. 13 ou 13Z), nom rue, code postal (5 chiffres), ville
    match = re.match(r"^([0-9]+[A-Z0-9]*)\s+(.*?)\s+(\d{5})\s+.+$", adresse)
    if match:
        numero = match.group(1)
        nom_rue = match.group(2)
        return numero, nom_rue
    return "", ""

def nettoyer_prefixe_numero(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime le préfixe 'numero_voie_ban' si présent en début de 'nom_rue_ban'."""
    def remove_prefix(row):
        numero = str(row["numero_voie_ban"]).strip()
        nom_rue = str(row["nom_rue_ban"]).strip()
        if numero and nom_rue.startswith(numero):
            return nom_rue[len(numero):].lstrip()
        return nom_rue
    
    df["nom_rue_ban"] = df.apply(remove_prefix, axis=1)
    return df

def nettoyer_dpe(input_file: str, output_file: str, sep: str = ";"):
    """Nettoie les colonnes adresse/numero/nom_rue dans le DPE."""
    df = pd.read_csv(input_file, sep=sep, dtype=str, low_memory=False)

    # Normaliser colonnes si absentes
    for col in ["adresse_ban", "numero_voie_ban", "nom_rue_ban"]:
        if col not in df.columns:
            df[col] = ""

    # Nettoyage de base
    df["adresse_ban"] = df["adresse_ban"].fillna("").apply(nettoyer_texte)
    df["numero_voie_ban"] = df["numero_voie_ban"].fillna("").apply(nettoyer_texte)
    df["nom_rue_ban"] = df["nom_rue_ban"].fillna("").apply(nettoyer_texte)

    # Compléter numero/nom_rue si vide, depuis adresse_ban
    for idx, row in df.iterrows():
        if (not row["numero_voie_ban"] or not row["nom_rue_ban"]) and row["adresse_ban"]:
            numero, nom_rue = extraire_depuis_adresse(row["adresse_ban"])
            if not row["numero_voie_ban"]:
                df.at[idx, "numero_voie_ban"] = numero
            if not row["nom_rue_ban"]:
                df.at[idx, "nom_rue_ban"] = nom_rue

    # Supprimer numero en doublon au début de la rue
    df = nettoyer_prefixe_numero(df)

    # Sauvegarde
    df.to_csv(output_file, index=False, sep=sep)
    print(f"✅ Fichier DPE nettoyé sauvegardé : {output_file} ({len(df)} lignes)")

# Exemple d'utilisation
nettoyer_dpe("ressources/dpe/dpe03existant.csv", "nettoyage/dpe_clean.csv", sep=",")
