import pandas as pd
from constants import expand_type_de_voie_column, _normalize_abbr, detect_type_in_voie

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
        "Type local": "type_local",
        "Surface reelle bati": "surface_reelle_bati",
        "Nombre pieces principales": "nombre_pieces_principales",
        "No voie": "numero_voie",
        "Type de voie": "type_voie",
        "Voie": "voie",
        "Code departement": "code_departement",
        "Code commune": "code_commune"
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
    
    # Filtres puis copy() pour éviter SettingWithCopyWarning
    df_filtre = df[
        (df["nature_mutation"].isin(["Vente", "Vente en l’état futur d’achèvement"])) &
        (df["valeur_fonciere"] >= 10000) &
        (df["type_local"].isin(["Maison"])) &
        (df["surface_reelle_bati"] >= 9) &
        (df["nombre_pieces_principales"].between(1, 8)) # &
        # (df["code_postal"].str.match(r"^91\d{3}$", na=False))
    ].copy()
    
    # Remplissage des zéros pour code département et code commune
    df_filtre.loc[:, "code_departement"] = df_filtre["code_departement"].str.zfill(2)
    df_filtre.loc[:, "code_commune"] = df_filtre["code_commune"].str.zfill(3)
    
    # Création colonne code_insee
    df_filtre.loc[:, "code_insee"] = df_filtre["code_departement"] + df_filtre["code_commune"]
    
    # Conversion des abréviations en mots complets dans type_voie
    df_filtre.loc[:, "type_voie"] = expand_type_de_voie_column(df_filtre["type_voie"])
    
    # Nettoyage de la colonne voie (remplacer '-' et "'" par un espace)
    df_filtre.loc[:, "voie"] = (
        df_filtre["voie"]
        .str.replace("-", " ", regex=False)
        .str.replace("'", " ", regex=False)
    )

    # Limiter à max_rows lignes
    df_filtre = df_filtre.head(max_rows)
    
    # Sauvegarde en CSV avec séparateur ","
    df_filtre.to_csv(output_file, index=False, sep=",")
    print(f"✅ Fichier nettoyé sauvegardé : {output_file} ({len(df_filtre)} lignes)")

# Exemple d'utilisation
chemin_dvf = "ressources/dvf/"
chemin_sauvegarde = "nettoyage/"
nettoyer_dvf(chemin_dvf + "ValeursFoncieres-2023.csv", chemin_sauvegarde + "dvf_filtre_2023.csv", 1000000)
nettoyer_dvf(chemin_dvf + "ValeursFoncieres-2022.csv", chemin_sauvegarde + "dvf_filtre_2022.csv", 1000000)
nettoyer_dvf(chemin_dvf + "ValeursFoncieres-2024.csv", chemin_sauvegarde + "dvf_filtre_2024.csv", 1000000)
