import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import unidecode

# --- Fonction normalisation ---
def normalize(text):
    if pd.isna(text):
        return ""
    return unidecode.unidecode(str(text)).upper().strip().replace(" ", "")

# --- Chargement des fichiers ---
fichier_dpe = "nettoyage/dpe_clean.csv"
fichier_dvf = "nettoyage/dvf_filtre_2022.csv"

dpe = pd.read_csv(fichier_dpe, dtype=str)
dvf = pd.read_csv(fichier_dvf, dtype=str)

# --- Nettoyage ---
dvf["valeur_fonciere"] = pd.to_numeric(dvf["valeur_fonciere"], errors="coerce")

map_dpe = {letter: i+1 for i, letter in enumerate("ABCDEFG")}
dpe["score_dpe"] = dpe["etiquette_dpe"].map(map_dpe)

# --- Identifiants uniques ---
dpe["id_adresse"] = (
    dpe["numero_voie_ban"].fillna("").apply(normalize) + "_" +
    dpe["nom_rue_ban"].fillna("").apply(normalize) + "_" +
    dpe["code_insee_ban"].fillna("").apply(normalize)
)

dvf["id_adresse"] = (
    dvf["numero_voie"].fillna("").apply(normalize) + "_" +
    dvf["type_de_voie"].fillna("").apply(normalize) + "_" +
    dvf["voie"].fillna("").apply(normalize) + "_" +
    dvf["code_insee"].fillna("").apply(normalize)
)

# --- Jointure ---
df_merge = pd.merge(dpe, dvf, on="id_adresse", how="inner")

df_merge = df_merge.dropna(subset=["score_dpe", "valeur_fonciere"])

# --- Corrélations ---
pearson_corr, _ = pearsonr(df_merge["score_dpe"], df_merge["valeur_fonciere"])
spearman_corr, _ = spearmanr(df_merge["score_dpe"], df_merge["valeur_fonciere"])

print("Corrélation Pearson (avec identifiant):", pearson_corr)
print("Corrélation Spearman (avec identifiant):", spearman_corr)

# --- Visualisation ---
plt.figure(figsize=(12,5))

# Scatterplot
plt.subplot(1,2,1)
sns.scatterplot(x="score_dpe", y="valeur_fonciere", data=df_merge, alpha=0.5)
plt.title("Scatterplot - Valeur foncière vs Score DPE (avec identifiant)")
plt.xlabel("Score DPE (A=1 ... G=7)")
plt.ylabel("Valeur foncière (€)")

# Boxplot
plt.subplot(1,2,2)
sns.boxplot(x="etiquette_dpe", y="valeur_fonciere", data=df_merge)
plt.title("Boxplot - Valeur foncière par classe DPE (avec identifiant)")
plt.xlabel("Classe DPE")
plt.ylabel("Valeur foncière (€)")

plt.tight_layout()
plt.show()
