import pandas as pd
import unidecode

def nettoyer_dvf(input_file, output_file, max_rows=10000):
    # Lecture avec séparateur pipe
    df = pd.read_csv(input_file, sep="|", dtype=str, low_memory=False)
    
    # Renommer colonnes qu'on veut garder
    mapping = {
        "Nature mutation": "nature_mutation",
        "Date mutation": "date_mutation",
        "Valeur fonciere": "valeur_fonciere",
        "Code postal": "code_postal",
        "Commune": "commune",
        "Code departement": "code_departement",
        "Type local": "type_local",
        "Surface reelle bati": "surface_reelle_bati",
        "Nombre pieces principales": "nombre_pieces_principales"
    }
    df = df.rename(columns=mapping)
    
    # Ne garder que les colonnes utiles
    df = df[list(mapping.values())]
    
    # Conversion des colonnes numériques
    df["valeur_fonciere"] = (
        df["valeur_fonciere"].str.replace(",", ".", regex=False)
    )
    df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
    df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
    df["nombre_pieces_principales"] = pd.to_numeric(df["nombre_pieces_principales"], errors="coerce")
    
    # Filtres
    df_filtre = df[
        (df["nature_mutation"].isin(["Vente", "Vente en l’état futur d’achèvement"])) &
        (df["valeur_fonciere"] >= 10000) &
        (df["type_local"].isin(["Maison"])) &
        (df["surface_reelle_bati"] >= 9) &
        (df["nombre_pieces_principales"].between(1, 8)) &
        (df["code_postal"].str.startswith("91", na=False))
    ]
    
    # Limiter à 10 000 lignes
    df_filtre = df_filtre.head(max_rows)
    
    # Sauvegarde en CSV avec séparateur ";"
    df_filtre.to_csv(output_file, index=False, sep=";")
    print(f"✅ Fichier nettoyé sauvegardé : {output_file} ({len(df_filtre)} lignes)")

# Exemple d'utilisation
chemin_dvf = "ressources/dvf/"
nettoyer_dvf(chemin_dvf + "ValeursFoncieres-2023.csv", "dvf_filtre_91.csv")
