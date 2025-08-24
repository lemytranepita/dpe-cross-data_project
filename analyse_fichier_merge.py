import pandas as pd
import numpy as np

def stats_et_comptage_par_note_dpe(fichier_csv):
    # Charger le fichier CSV
    df = pd.read_csv(fichier_csv, delimiter=',', encoding='utf-8')

    # Vérifier que les colonnes nécessaires existent
    colonnes_requises = ['etiquette_dpe', 'annee_construction']
    if not all(col in df.columns for col in colonnes_requises):
        raise ValueError("Le fichier CSV ne contient pas les colonnes requises.")

    # Compter les biens sans année de construction (valeurs manquantes ou invalides)
    df_sans_annee = df[df['annee_construction'].isna() | (df['annee_construction'].apply(lambda x: str(x).strip() == ''))]
    comptage_sans_annee = df_sans_annee.groupby('etiquette_dpe').size().rename('sans_annee')

    # Nettoyer les données : supprimer les lignes où l'année de construction est manquante ou invalide
    df = df.dropna(subset=['annee_construction'])
    df['annee_construction'] = pd.to_numeric(df['annee_construction'], errors='coerce')
    df = df.dropna(subset=['annee_construction'])

    # Convertir l'année de construction en entier
    df['annee_construction'] = df['annee_construction'].astype(int)

    # Calculer les statistiques pour chaque note de DPE
    stats = df.groupby('etiquette_dpe')['annee_construction'].agg(
        ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75), 'count']
    )
    stats.columns = ['moyenne', 'mediane', 'Q1', 'Q3', 'nombre_logements']

    # Arrondir et convertir en entier
    stats['moyenne'] = stats['moyenne'].round().astype(int)
    stats['mediane'] = stats['mediane'].astype(int)
    stats['Q1'] = stats['Q1'].round().astype(int)
    stats['Q3'] = stats['Q3'].round().astype(int)
    stats['nombre_logements'] = stats['nombre_logements'].astype(int)

    # Fusionner avec le comptage des biens sans année de construction
    stats = stats.join(comptage_sans_annee, how='outer').fillna(0)
    stats['sans_annee'] = stats['sans_annee'].astype(int)

    return stats

# Exemple d'utilisation
fichier_csv = "correlation/dpe_dvf_merge.csv"  # Remplace par le chemin de ton fichier
resultat = stats_et_comptage_par_note_dpe(fichier_csv)
print(resultat)
