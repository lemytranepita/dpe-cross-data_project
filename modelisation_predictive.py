# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import catboost as cb
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Charger les données
df = pd.read_csv("correlation/dpe_dvf_merge.csv", sep=",", encoding='utf-8')

# 2. Prétraitement
# Sélection des variables pertinentes
variables = [
    'valeur_fonciere', 'etiquette_dpe', 'surface_reelle_bati',
    'nombre_pieces_principales', 'annee_construction', 'code_postal'
]
df = df[variables].dropna()

# Transformation de l'étiquette DPE en numérique (A=1, B=2, ..., G=7)
dpe_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
df['etiquette_dpe'] = df['etiquette_dpe'].map(dpe_mapping)

# Séparation des variables explicatives (X) et de la cible (y)
X = df.drop('valeur_fonciere', axis=1)
y = df['valeur_fonciere']

# Liste des variables catégorielles pour CatBoost
cat_features = ['etiquette_dpe', 'code_postal']

# 3. Division en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraînement du modèle CatBoost
model = cb.CatBoostRegressor(
    cat_features=cat_features,
    verbose=100,
    random_state=42
)
model.fit(X_train, y_train)

# 5. Prédiction et évaluation
y_pred = model.predict(X_test)

# Calcul des métriques
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.2f}")

# 6. Importance des variables
feature_importances = model.get_feature_importance()
features = X.columns
importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Visualisation de l'importance des variables
plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title("Importance des variables dans la prédiction de la valeur foncière")
plt.tight_layout()
plt.savefig('correlation/importance_variables.png', bbox_inches='tight', dpi=100)
plt.close()
