import pandas as pd
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import os

# --- Chargement des fichiers ---
fichier_dpe = "nettoyage/dpe_clean.csv"
fichier_dvf = "nettoyage/dvf_filtre_2022.csv"

dpe = pd.read_csv(fichier_dpe, dtype=str)
dvf = pd.read_csv(fichier_dvf, dtype=str)

# --- Conversion valeur foncière en numérique ---
dvf["valeur_fonciere"] = pd.to_numeric(dvf["valeur_fonciere"], errors="coerce")

# --- Conversion DPE (A..H) en score numérique ---
map_dpe = {letter: i+1 for i, letter in enumerate("ABCDEFGH")}
dpe["score_dpe"] = dpe["etiquette_dpe"].map(map_dpe)

# --- Jointure sur adresse ---
df_merge = pd.merge(
    dpe,
    dvf,
    left_on=["numero_voie_ban", "nom_rue_ban", "code_insee_ban"],
    right_on=["numero_voie", "voie", "code_insee"],
    how="inner"
)

# --- Suppression des NA ---
df_merge = df_merge.dropna(subset=["score_dpe", "valeur_fonciere"])

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
df_merge.boxplot(column="valeur_fonciere", by="etiquette_dpe", 
                 positions=range(1, len("ABCDEFG")+1), 
                 widths=0.6, patch_artist=True)
plt.title("Valeur foncière par classe DPE")
plt.suptitle("")
plt.xlabel("Classe DPE")
plt.ylabel("Valeur foncière (€)")
plt.xticks(range(1, len("ABCDEFGH")+1), list("ABCDEFGH"))
plt.savefig("correlation/boxplot_valeur_vs_dpe.png", dpi=300)
plt.close()

# Scatter avec jitter
plt.figure(figsize=(10,6))
plt.scatter(df_merge["score_dpe"], df_merge["valeur_fonciere"], alpha=0.3)
plt.title("Corrélation Score DPE vs Valeur foncière")
plt.xlabel("Score DPE (A=1, G=7, H=8)")
plt.ylabel("Valeur foncière (€)")
plt.xticks(range(1, len("ABCDEFGH")+1), list("ABCDEFGH"))
plt.savefig("correlation/scatter_valeur_vs_dpe.png", dpi=300)
plt.close()

# Moyenne par DPE
plt.figure(figsize=(10,6))
df_merge.groupby("etiquette_dpe")["valeur_fonciere"].mean().reindex(list("ABCDEFGH")).plot(kind="bar")
plt.title("Valeur foncière moyenne par classe DPE")
plt.xlabel("Classe DPE")
plt.ylabel("Valeur foncière moyenne (€)")
plt.savefig("correlation/barplot_moyenne_valeur_vs_dpe.png", dpi=300)
plt.close()