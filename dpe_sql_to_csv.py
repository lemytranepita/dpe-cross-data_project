import psycopg2
import pandas as pd

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname="dpe",
    user="postgres",
    password="password",
    host="localhost",
#   host="192.168.0.100",
    port="5432"
)

query = """
SELECT DISTINCT ON (a.id)
    d.identifiant_dpe AS numero_dpe,
    a.ban_housenumber AS numero_voie_ban,
    a.ban_street AS nom_rue_ban,
    a.ban_city AS nom_commune_ban,
    a.ban_postcode AS code_postal_ban,
    d.date_etablissement_dpe,
    da.dpe_a_remplacer AS numero_dpe_remplace,
    da.enum_modele_dpe_id AS modele_dpe,
    cg.enum_methode_application_dpe_log_id AS methode_application_dpe,
    bc.classe_conso_energie AS etiquette_dpe,
    a.ban_label AS adresse_ban,
    a.ban_departement AS code_departement_ban,
    a.ban_citycode AS code_insee_ban,
    cg.annee_construction
FROM dpe d
JOIN dpe_administratif da ON da.dpe_id = d.id
JOIN dpe_geolocalisation g ON g.administratif_id = da.dpe_id
JOIN dpe_t_adresse a ON a.id = g.adresse_bien_id
JOIN dpe_bilan_consommation bc ON bc.dpe_id = d.id
JOIN dpe_caracteristique_generale cg ON cg.dpe_id = d.id
ORDER BY a.id, d.date_etablissement_dpe DESC;
"""

# Charger le résultat
df = pd.read_sql(query, conn)

# Export en CSV
df.to_csv("files/output/export_dpe.csv", index=False, sep="|", encoding="utf-8")

conn.close()