import os
import glob
import pandas as pd

# === 1. Créer les listes de fichiers ===
# Tous les CSV de DPE
dpe_files = glob.glob("ressources/dpe/*.csv")
# Tous les CSV de DVF
dvf_files = glob.glob("ressources/dvf/*.csv")

print("📂 Fichiers DPE :", dpe_files)
print("📂 Fichiers DVF :", dvf_files)


# === 2. Fonction pour créer un identifiant maison ===
def create_identifier(df, cols):
    """
    Crée un identifiant unique basé sur plusieurs colonnes concaténées.
    Exemple : numéro voie + nom voie + code postal + commune
    """
    df["identifiant"] = (
        df[cols[0]].astype(str).str.strip() + "_" +
        df[cols[1]].astype(str).str.strip() + "_" +
        df[cols[2]].astype(str).str.strip() + "_" +
        df[cols[3]].astype(str).str.strip()
    )
    return df


# === 3. Lecture en chunks pour éviter RAM saturée ===
def read_large_csv(filepath, sep="|", chunksize=100000):
    """
    Lit un CSV volumineux par morceaux (chunks).
    Retourne un générateur de DataFrames.
    """
    return pd.read_csv(filepath, sep=sep, chunksize=chunksize, low_memory=False)


# === 4. Exemple d’utilisation : charger et harmoniser ===
# Colonnes utiles (à adapter selon les fichiers exacts)
dpe_cols = ["numero_voie", "nom_rue", "code_postal", "nom_commune", "classe_consommation_energie"]
dvf_cols = ["NoVoie", "Voie", "CodePostal", "Commune", "ValeurFonciere"]

# Lecture du premier fichier DPE en mode chunks
for chunk in read_large_csv(dpe_files[0], sep=","):  # souvent DPE est en ";"
    df_dpe = chunk[dpe_cols].copy()
    df_dpe = create_identifier(df_dpe, ["numero_voie", "nom_rue", "code_postal", "nom_commune"])
    print(df_dpe.head())
    break  # on s'arrête au premier chunk juste pour test

# Lecture du premier fichier DVF en mode chunks
for chunk in read_large_csv(dvf_files[0], sep="|"):  # DVF est en "|"
    df_dvf = chunk[dvf_cols].copy()
    df_dvf = create_identifier(df_dvf, ["NoVoie", "Voie", "CodePostal", "Commune"])
    print(df_dvf.head())
    break
