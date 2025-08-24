# correlation_sans_id.py
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import os
import re

# --- Chargement des fichiers ---
fichier_dpe = "files/output/export_dpe_filtered.csv"
fichier_dvf = "files/output/dvf_filtered.csv"

dpe = pd.read_csv(fichier_dpe, dtype=str, delimiter="|")
dvf = pd.read_csv(fichier_dvf, dtype=str, delimiter="|")

# --- Conversion valeur foncière en numérique ---
dvf["valeur_fonciere"] = pd.to_numeric(dvf["valeur_fonciere"], errors="coerce")

# --- Conversion DPE (A..G) en score numérique ---
map_dpe = {letter: i+1 for i, letter in enumerate("ABCDEFG")}
dpe["score_dpe"] = dpe["etiquette_dpe"].map(map_dpe)

# --- Normaliser numéro de voie ---
def normaliser_numero(numero):
    if pd.isna(numero):
        return ""
    numero = str(numero).upper().replace(" ", "")
    numero = numero.replace("BIS", "B").replace("TER", "T")
    return numero

dpe["numero_voie_ban"] = dpe["numero_voie_ban"].apply(normaliser_numero)
dvf["numero_voie"] = dvf["numero_voie"].apply(normaliser_numero)

# --- Supprimer le type de voie dans DVF ---
def enlever_type_voie(voie):
    if pd.isna(voie):
        return ""
    voie = str(voie).upper()
    # Supprimer type de voie (ex : RUE, AVENUE, BOULEVARD, IMPASSE, etc.)
    voie = re.sub(r"^(RUE|AVENUE|BD|BOULEVARD|IMPASSE|ALLEE|CHEMIN|PLACE|QUAI|VOIE|ROUTE|SQUARE)\s+", "", voie)
    return voie.strip()

dvf["nom_rue_simplifie"] = dvf["voie"].apply(enlever_type_voie)
dpe["nom_rue_simplifie"] = dpe["nom_rue_ban"].apply(enlever_type_voie)

# --- Merge sur code postal, numéro et nom de rue simplifié ---
df_merge = pd.merge(
    dpe,
    dvf,
    left_on=["code_postal_ban", "numero_voie_ban", "nom_rue_simplifie"],
    right_on=["code_postal", "numero_voie", "nom_rue_simplifie"],
    how="inner"
)

# --- Suppression des NA ---
df_merge = df_merge.dropna(subset=["score_dpe", "valeur_fonciere"])

# --- Suppression des doublons sur le numéro de DPE ---
df_merge = df_merge.drop_duplicates(subset=["numero_voie_ban"])

# --- Création du dossier de sortie ---
os.makedirs("correlation", exist_ok=True)

# --- Sauvegarde du merge ---
df_merge.to_csv("correlation/dpe_dvf_merge.csv", index=False)

# --- Corrélations ---
pearson_corr, _ = pearsonr(df_merge["score_dpe"], df_merge["valeur_fonciere"])
spearman_corr, _ = spearmanr(df_merge["score_dpe"], df_merge["valeur_fonciere"])

with open("correlation/resultats_corr.txt", "w") as f:
    f.write(f"Corrélation Pearson : {pearson_corr}\n")
    f.write(f"Corrélation Spearman : {spearman_corr}\n")

print("Corrélation Pearson :", pearson_corr)
print("Corrélation Spearman :", spearman_corr)

# --- Visualisations ---
plt.figure(figsize=(10,6))
classes_presentes = sorted(df_merge['etiquette_dpe'].dropna().unique())
df_merge.boxplot(
    column="valeur_fonciere",
    by="etiquette_dpe",
    positions=range(1, len(classes_presentes)+1),
    widths=0.6,
    patch_artist=True,
    showfliers=False  # <-- Désactive l'affichage des outliers
)
plt.xticks(range(1, len(classes_presentes)+1), classes_presentes)
plt.title("Valeur foncière par classe DPE")
plt.suptitle("")
plt.xlabel("Classe DPE")
plt.ylabel("Valeur foncière (€)")
plt.xticks(range(1, len("ABCDEFG")+1), list("ABCDEFG"))
plt.ylim(0, 2000000)
plt.savefig("correlation/boxplot_valeur_vs_dpe.png", dpi=300)
plt.close()


# Scatter
plt.figure(figsize=(10,6))
plt.scatter(df_merge["score_dpe"], df_merge["valeur_fonciere"], alpha=0.3)
plt.title("Corrélation Score DPE vs Valeur foncière")
plt.xlabel("Score DPE (A=1, G=7)")
plt.ylabel("Valeur foncière (€)")
plt.xticks(range(1, len("ABCDEFG")+1), list("ABCDEFG"))
plt.savefig("correlation/scatter_valeur_vs_dpe.png", dpi=300)
plt.close()

# Moyenne par DPE
plt.figure(figsize=(10,6))
df_merge.groupby("etiquette_dpe")["valeur_fonciere"].mean().reindex(list("ABCDEFG")).plot(kind="bar")
plt.title("Valeur foncière moyenne par classe DPE")
plt.xlabel("Classe DPE")
plt.ylabel("Valeur foncière moyenne (€)")
plt.savefig("correlation/barplot_moyenne_valeur_vs_dpe.png", dpi=300)
plt.close()
